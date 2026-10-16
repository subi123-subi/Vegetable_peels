import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';

class SafetyInformationScreen extends ConsumerWidget {
  const SafetyInformationScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final veg = ref.watch(selectedVegetableProvider);
    final safetyRules = ref.watch(safetyRulesForSelectedVegetableProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'உணவு பாதுகாப்பு பகுப்பாய்வு' : 'Food Safety Evaluation'),
        backgroundColor: Colors.orange.shade800,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/nutrients'),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 800),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Critical Safety Warning Banner
                Container(
                  padding: const EdgeInsets.all(18),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: Colors.red.shade200),
                  ),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.gpp_maybe_rounded, color: Colors.red, size: 28),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              isTamil ? 'முக்கிய பாதுகாப்பு விதிமுறை' : 'Core Food Safety Directive',
                              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Colors.red),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              isTamil
                                  ? 'புகைப்பட தோற்றம் மட்டுமே காய்கறி தோலை உண்ண பாதுகாப்பானது என்று சான்றளிக்காது. தெரியாத பூச்சிக்கொல்லிகள் அல்லது அழுகல் இருந்தால் எப்போதும் உரமாக்கல் அல்லது கழிவுநீக்கத்திற்கு மாற்றுங்கள்.'
                                  : 'Never use camera appearance alone to certify a peel as safe to eat. If microbial spoilage, greening, or unknown pesticide history is suspected, divert conservatively to composting.',
                              style: TextStyle(color: Colors.red.shade900, fontSize: 12, height: 1.3),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),

                // Vegetable Status Header
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              veg.displayName(isTamil),
                              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                              decoration: BoxDecoration(
                                color: veg.foodSafetyStatus == 'hazardous_raw'
                                    ? Colors.red.shade100
                                    : veg.foodSafetyStatus == 'conditional_cooking_required'
                                        ? Colors.orange.shade100
                                        : Colors.green.shade100,
                                borderRadius: BorderRadius.circular(10),
                              ),
                              child: Text(
                                veg.foodSafetyStatus.replaceAll('_', ' ').toUpperCase(),
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 11,
                                  color: veg.foodSafetyStatus == 'hazardous_raw'
                                      ? Colors.red.shade900
                                      : veg.foodSafetyStatus == 'conditional_cooking_required'
                                          ? Colors.orange.shade900
                                          : Colors.green.shade900,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          isTamil ? (veg.knownHazardsTa ?? 'தெரிந்த அபாயங்கள் எதுவும் இல்லை.') : (veg.knownHazardsEn ?? 'No special chemical hazards noted.'),
                          style: TextStyle(fontSize: 13, color: Colors.grey.shade800, height: 1.3),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // Active Safety Rules
                Text(
                  isTamil ? 'செயலில் உள்ள அறிவியல் பாதுகாப்பு விதிகள்:' : 'Enforced Scientific Safety Rules:',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: AppTheme.primaryDark),
                ),
                const SizedBox(height: 10),

                ...safetyRules.map((rule) => Card(
                  child: Padding(
                    padding: const EdgeInsets.all(18.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(
                              rule.severity == 'critical'
                                  ? Icons.dangerous
                                  : rule.severity == 'warning'
                                      ? Icons.warning
                                      : Icons.info,
                              color: rule.severity == 'critical'
                                  ? Colors.red
                                  : rule.severity == 'warning'
                                      ? Colors.orange.shade800
                                      : Colors.blue,
                              size: 20,
                            ),
                            const SizedBox(width: 8),
                            Text(
                              '${rule.hazardType.toUpperCase()} (${rule.severity.toUpperCase()})',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 13,
                                color: rule.severity == 'critical' ? Colors.red : Colors.orange.shade900,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          rule.displayDescription(isTamil),
                          style: const TextStyle(fontSize: 13, height: 1.3),
                        ),
                        if (rule.displayAlternative(isTamil).isNotEmpty) ...[
                          const SizedBox(height: 10),
                          Container(
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: AppTheme.softMint,
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Row(
                              children: [
                                const Icon(Icons.eco, size: 16, color: AppTheme.primaryGreen),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: Text(
                                    'Conservative Alternative: ${rule.displayAlternative(isTamil)}',
                                    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppTheme.primaryDark),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                )),
                const SizedBox(height: 20),

                ElevatedButton.icon(
                  onPressed: () => context.go('/waste-reuse'),
                  icon: const Icon(Icons.recycling),
                  label: Text(isTamil ? 'பாதுகாப்பான பயன்பாட்டு முறைகளைக் காண்க' : 'View Safe Valorization Alternatives'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.primaryGreen,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
