import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../models/app_models.dart';
import '../../providers/app_providers.dart';
import '../../providers/scan_provider.dart';

class VegetableIdentificationScreen extends ConsumerStatefulWidget {
  const VegetableIdentificationScreen({super.key});

  @override
  ConsumerState<VegetableIdentificationScreen> createState() =>
      _VegetableIdentificationScreenState();
}

class _VegetableIdentificationScreenState
    extends ConsumerState<VegetableIdentificationScreen> {
  VegetableItem? _selectedCorrection;
  bool _isConfirming = false;

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final currentScan = ref.watch(currentScanProvider);
    final scanPredAsync = ref.watch(scanPredictionProvider);
    final catalogue = ref.watch(catalogueProvider);

    final aiResult = scanPredAsync.value;

    // Fallbacks
    final VegetableItem fallbackVeg =
        currentScan?.predictedVegetable ?? ref.watch(selectedVegetableProvider);
    final VegetableItem activeVeg = _selectedCorrection ?? fallbackVeg;
    final double confidence = aiResult?.confidence ?? currentScan?.confidence ?? 0.94;
    final bool isSupported = aiResult?.isSupportedPeel ?? true;
    final bool isUncertain = aiResult?.isUncertain ?? (confidence < 0.65);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 700),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Image Preview Card if available
              if (aiResult?.localImageBytes != null)
                Card(
                  clipBehavior: Clip.antiAlias,
                  child: Stack(
                    alignment: Alignment.bottomRight,
                    children: [
                      Image.memory(
                        aiResult!.localImageBytes!,
                        height: 200,
                        width: double.infinity,
                        fit: BoxFit.cover,
                      ),
                      Container(
                        margin: const EdgeInsets.all(12),
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.black87,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          'Scanned Peel',
                          style: const TextStyle(color: Colors.white, fontSize: 11),
                        ),
                      ),
                    ],
                  ),
                ),
              if (aiResult?.localImageBytes != null) const SizedBox(height: 16),

              // Rejection / Uncertainty Warning Banner
              if (!isSupported || isUncertain)
                Container(
                  margin: const EdgeInsets.only(bottom: 16),
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.amber.shade50,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.amber.shade400, width: 1.5),
                  ),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Icon(Icons.warning_amber_rounded, color: Colors.amber.shade900, size: 28),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              isTamil
                                  ? 'குறைந்த நம்பிக்கை அல்லது ஆதரிக்கப்படாத பொருள்!'
                                  : 'Low Confidence / Unsupported Material',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 14,
                                color: Colors.amber.shade900,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              isTamil
                                  ? 'இந்த புகைப்படம் காய்கறி தோலாக தெளிவாக தெரியவில்லை அல்லது 65% நம்பிக்கை எல்லைக்கு கீழ் உள்ளது. சரியான காய்கறியை கீழே தேர்வு செய்து தொடரவும்.'
                                  : 'The captured image has confidence below 65% or matches non-peel objects. Please manually select the confirmed vegetable below before proceeding.',
                              style: TextStyle(fontSize: 12, color: Colors.brown.shade800),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

              // Identification Result Card
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                            decoration: BoxDecoration(
                              color: AppTheme.softMint,
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Row(
                              children: [
                                const Icon(Icons.psychology, size: 16, color: AppTheme.primaryGreen),
                                const SizedBox(width: 6),
                                Text(
                                  aiResult != null
                                      ? 'MobileNetV3 (${aiResult.modelVersion})'
                                      : 'MobileNetV3 (v1.0.0)',
                                  style: const TextStyle(
                                    color: AppTheme.primaryDark,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 12,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                            decoration: BoxDecoration(
                              color: confidence >= 0.65 ? Colors.green.shade50 : Colors.red.shade50,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(
                                color: confidence >= 0.65 ? Colors.green.shade200 : Colors.red.shade200,
                              ),
                            ),
                            child: Text(
                              '${(confidence * 100).toStringAsFixed(1)}% Confidence',
                              style: TextStyle(
                                color: confidence >= 0.65 ? Colors.green.shade800 : Colors.red.shade900,
                                fontWeight: FontWeight.bold,
                                fontSize: 13,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),
                      Text(
                        isTamil ? 'கண்டறியப்பட்ட காய்கறி தோல்:' : 'Identified Vegetable Peel:',
                        style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        activeVeg.displayName(isTamil),
                        style: const TextStyle(
                          fontSize: 26,
                          fontWeight: FontWeight.bold,
                          color: AppTheme.primaryDark,
                        ),
                      ),
                      Text(
                        '${activeVeg.scientificName} • ${activeVeg.plantPart}',
                        style: TextStyle(
                          fontSize: 14,
                          fontStyle: FontStyle.italic,
                          color: Colors.grey.shade700,
                        ),
                      ),
                      const SizedBox(height: 16),

                      // Confidence Meter Bar
                      ClipRRect(
                        borderRadius: BorderRadius.circular(8),
                        child: LinearProgressIndicator(
                          value: confidence.clamp(0.0, 1.0),
                          minHeight: 8,
                          backgroundColor: Colors.grey.shade200,
                          valueColor: AlwaysStoppedAnimation<Color>(
                            confidence >= 0.65 ? AppTheme.primaryGreen : Colors.orange,
                          ),
                        ),
                      ),
                      const SizedBox(height: 16),

                      // Ranked alternative predictions
                      if (aiResult != null && aiResult.topPredictions.isNotEmpty) ...[
                        Text(
                          isTamil ? 'சாத்தியமான மற்ற வகைகள்:' : 'Alternative Predictions (Top Candidates):',
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
                        ),
                        const SizedBox(height: 8),
                        ...aiResult.topPredictions.take(3).map((candidate) {
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 6.0),
                            child: Row(
                              children: [
                                Expanded(
                                  flex: 3,
                                  child: Text(
                                    candidate.displayName(isTamil),
                                    style: const TextStyle(fontSize: 12),
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                                Expanded(
                                  flex: 4,
                                  child: ClipRRect(
                                    borderRadius: BorderRadius.circular(4),
                                    child: LinearProgressIndicator(
                                      value: candidate.confidence,
                                      minHeight: 6,
                                      backgroundColor: Colors.grey.shade100,
                                      valueColor: AlwaysStoppedAnimation<Color>(
                                        candidate.isSupportedPeel ? Colors.teal : Colors.grey,
                                      ),
                                    ),
                                  ),
                                ),
                                const SizedBox(width: 8),
                                Text(
                                  '${(candidate.confidence * 100).toStringAsFixed(1)}%',
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w600,
                                    color: Colors.grey.shade700,
                                  ),
                                ),
                              ],
                            ),
                          );
                        }),
                        const SizedBox(height: 16),
                      ],

                      // Safety Pre-Check Pill
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: activeVeg.foodSafetyStatus == 'hazardous_raw'
                              ? Colors.red.shade50
                              : activeVeg.foodSafetyStatus == 'conditional_cooking_required'
                                  ? Colors.orange.shade50
                                  : Colors.green.shade50,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Row(
                          children: [
                            Icon(
                              activeVeg.foodSafetyStatus == 'hazardous_raw'
                                  ? Icons.dangerous_rounded
                                  : activeVeg.foodSafetyStatus == 'conditional_cooking_required'
                                      ? Icons.warning_amber_rounded
                                      : Icons.check_circle_outline,
                              color: activeVeg.foodSafetyStatus == 'hazardous_raw'
                                  ? Colors.red
                                  : activeVeg.foodSafetyStatus == 'conditional_cooking_required'
                                      ? Colors.orange.shade800
                                      : AppTheme.primaryGreen,
                            ),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Text(
                                activeVeg.foodSafetyStatus == 'hazardous_raw'
                                    ? (isTamil
                                        ? 'அபாய எச்சரிக்கை: சமையலுக்கு பாதுகாப்பற்றது! உரமாக்கலுக்கு மட்டும்.'
                                        : 'Safety Flag: Inedible raw. Divert strictly to valorization/compost.')
                                    : activeVeg.foodSafetyStatus == 'conditional_cooking_required'
                                        ? (isTamil
                                            ? 'சமையல் எச்சரிக்கை: சமைக்க வேண்டும்; பச்சையாக உண்ணக்கூடாது.'
                                            : 'Safety Flag: Must be thoroughly cooked prior to consumption.')
                                        : (isTamil
                                            ? 'பாதுகாப்பானது: சமைக்க மற்றும் உண்ண ஏற்றது (கழுவ வேண்டும்).'
                                            : 'Safety Flag: Food-safe peel when properly washed.'),
                                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // Confirmation & Manual Correction Form
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        isTamil ? 'அடையாளத்தை உறுதிப்படுத்துங்கள்:' : 'User Confirmation Step:',
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        isTamil
                            ? 'ஏஐ முடிவில் ஏதேனும் தவறு இருப்பின், கீழேயுள்ள பட்டியலிலிருந்து சரியான காய்கறியைத் தேர்வு செய்யவும்.'
                            : 'If the AI prediction is incorrect, select the actual vegetable from the catalogue below.',
                        style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                      ),
                      const SizedBox(height: 16),
                      DropdownButtonFormField<VegetableItem>(
                        initialValue: activeVeg,
                        isExpanded: true,
                        decoration: InputDecoration(
                          labelText: isTamil ? 'காய்கறி தேர்வு செய்க' : 'Select Confirmed Vegetable',
                          prefixIcon: const Icon(Icons.eco),
                        ),
                        items: catalogue.map((veg) {
                          return DropdownMenuItem<VegetableItem>(
                            value: veg,
                            child: Text(
                              '${veg.displayName(isTamil)} (${veg.scientificName})',
                              overflow: TextOverflow.ellipsis,
                            ),
                          );
                        }).toList(),
                        onChanged: (val) {
                          if (val != null) {
                            setState(() {
                              _selectedCorrection = val;
                            });
                          }
                        },
                      ),
                      const SizedBox(height: 24),
                      Row(
                        children: [
                          Expanded(
                            child: OutlinedButton.icon(
                              onPressed: () => context.go('/camera-scan'),
                              icon: const Icon(Icons.replay),
                              label: Text(isTamil ? 'மறு ஸ்கேன்' : 'Retake'),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: ElevatedButton.icon(
                              onPressed: _isConfirming
                                  ? null
                                  : () async {
                                      setState(() => _isConfirming = true);
                                      if (aiResult != null && aiResult.scanId > 0) {
                                        await ref
                                            .read(scanPredictionProvider.notifier)
                                            .confirmPrediction(
                                              scanId: aiResult.scanId,
                                              confirmedVegetableId: activeVeg.id,
                                              isCorrection: _selectedCorrection != null,
                                              notes: 'User confirmed via identification screen',
                                            );
                                      }

                                      ref
                                          .read(currentScanProvider.notifier)
                                          .confirmVegetable(activeVeg);
                                      ref
                                          .read(selectedVegetableProvider.notifier)
                                          .select(activeVeg);

                                      if (!mounted) return;
                                      setState(() => _isConfirming = false);
                                      if (context.mounted) {
                                        context.go('/nutrients');
                                      }
                                    },
                              icon: _isConfirming
                                  ? const SizedBox(
                                      width: 16,
                                      height: 16,
                                      child: CircularProgressIndicator(
                                        strokeWidth: 2,
                                        color: Colors.white,
                                      ),
                                    )
                                  : const Icon(Icons.check),
                              label: Text(isTamil ? 'உறுதி செய்க' : 'Confirm & Proceed'),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
