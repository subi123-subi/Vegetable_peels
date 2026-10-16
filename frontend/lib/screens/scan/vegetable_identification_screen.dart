import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../models/app_models.dart';
import '../../providers/app_providers.dart';

class VegetableIdentificationScreen extends ConsumerStatefulWidget {
  const VegetableIdentificationScreen({super.key});

  @override
  ConsumerState<VegetableIdentificationScreen> createState() => _VegetableIdentificationScreenState();
}

class _VegetableIdentificationScreenState extends ConsumerState<VegetableIdentificationScreen> {
  VegetableItem? _selectedCorrection;

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final currentScan = ref.watch(currentScanProvider);
    final catalogue = ref.watch(catalogueProvider);

    // If no scan active, fallback to selected vegetable
    final VegetableItem predictedVeg = currentScan?.predictedVegetable ?? ref.watch(selectedVegetableProvider);
    final VegetableItem activeVeg = _selectedCorrection ?? predictedVeg;
    final confidence = currentScan?.confidence ?? 0.94;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 700),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
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
                                  'MobileNetV3 (v1.0.0)',
                                  style: const TextStyle(color: AppTheme.primaryDark, fontWeight: FontWeight.bold, fontSize: 12),
                                ),
                              ],
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                            decoration: BoxDecoration(
                              color: confidence > 0.85 ? Colors.green.shade50 : Colors.amber.shade50,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: confidence > 0.85 ? Colors.green.shade200 : Colors.amber.shade200),
                            ),
                            child: Text(
                              '${(confidence * 100).toStringAsFixed(1)}% Match',
                              style: TextStyle(
                                color: confidence > 0.85 ? Colors.green.shade800 : Colors.amber.shade900,
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
                        style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                      ),
                      Text(
                        '${activeVeg.scientificName} • ${activeVeg.plantPart}',
                        style: TextStyle(fontSize: 14, fontStyle: FontStyle.italic, color: Colors.grey.shade700),
                      ),
                      const SizedBox(height: 16),

                      // Confidence Meter Bar
                      ClipRRect(
                        borderRadius: BorderRadius.circular(8),
                        child: LinearProgressIndicator(
                          value: confidence,
                          minHeight: 8,
                          backgroundColor: Colors.grey.shade200,
                          valueColor: AlwaysStoppedAnimation<Color>(
                            confidence > 0.85 ? AppTheme.primaryGreen : Colors.orange,
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),

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
                                    ? (isTamil ? 'அபாய எச்சரிக்கை: சமையலுக்கு பாதுகாப்பற்றது! உரமாக்கலுக்கு மட்டும்.' : 'Safety Flag: Inedible raw. Divert strictly to valorization/compost.')
                                    : activeVeg.foodSafetyStatus == 'conditional_cooking_required'
                                        ? (isTamil ? 'சமையல் எச்சரிக்கை: சமைக்க வேண்டும்; பச்சையாக உண்ணக்கூடாது.' : 'Safety Flag: Must be thoroughly cooked prior to consumption.')
                                        : (isTamil ? 'பாதுகாப்பானது: சமைக்க மற்றும் உண்ண ஏற்றது (கழுவ வேண்டும்).' : 'Safety Flag: Food-safe peel when properly washed.'),
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
                        decoration: InputDecoration(
                          labelText: isTamil ? 'காய்கறி தேர்வு செய்க' : 'Select Confirmed Vegetable',
                          prefixIcon: const Icon(Icons.eco),
                        ),
                        items: catalogue.map((veg) {
                          return DropdownMenuItem<VegetableItem>(
                            value: veg,
                            child: Text('${veg.displayName(isTamil)} (${veg.scientificName})'),
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
                              onPressed: () {
                                ref.read(currentScanProvider.notifier).confirmVegetable(activeVeg);
                                ref.read(selectedVegetableProvider.notifier).select(activeVeg);
                                context.go('/nutrients');
                              },
                              icon: const Icon(Icons.check),
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
