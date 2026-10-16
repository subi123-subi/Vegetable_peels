import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';

class WasteReuseScreen extends ConsumerWidget {
  const WasteReuseScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final veg = ref.watch(selectedVegetableProvider);
    final reuseMethods = ref.watch(reuseMethodsForSelectedVegetableProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'கழிவு மறுபயன்பாடு & மதிப்புக்கூட்டல்' : 'Valorization & Waste Reuse'),
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
                // Header Banner
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Row(
                      children: [
                        CircleAvatar(
                          radius: 26,
                          backgroundColor: AppTheme.softMint,
                          child: const Icon(Icons.recycling_rounded, color: AppTheme.primaryGreen, size: 28),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                '${veg.displayName(isTamil)} Valorization',
                                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                              ),
                              Text(
                                isTamil
                                    ? 'அறிவியல் சான்றுகளின் அடிப்படையில் பாதுகாப்பான மறுபயன்பாட்டு வழிகள்'
                                    : 'Ranked by evidence hierarchy and biological safety constraints',
                                style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // Ranked Reuse Cards
                ...reuseMethods.map((method) => Card(
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Row(
                              children: [
                                CircleAvatar(
                                  radius: 14,
                                  backgroundColor: AppTheme.primaryGreen,
                                  child: Text(
                                    '#${method.evidenceRank}',
                                    style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                                  ),
                                ),
                                const SizedBox(width: 10),
                                Text(
                                  method.displayName(isTamil),
                                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                                ),
                              ],
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                              decoration: BoxDecoration(
                                color: AppTheme.softMint,
                                borderRadius: BorderRadius.circular(6),
                              ),
                              child: Text(
                                method.category,
                                style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        Text(
                          method.displayInstructions(isTamil),
                          style: TextStyle(fontSize: 13, color: Colors.grey.shade800, height: 1.4),
                        ),
                        const SizedBox(height: 16),
                        OutlinedButton.icon(
                          onPressed: () {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text(isTamil ? 'திசைதிருப்பல் வெற்றி! உங்கள் கழிவு பதிவில் சேர்க்கப்பட்டது.' : 'Diversion confirmed! Added to your smart waste diversion log.'),
                                backgroundColor: AppTheme.primaryGreen,
                              ),
                            );
                          },
                          icon: const Icon(Icons.check_circle_outline, size: 16),
                          label: Text(isTamil ? 'இம்முறையைப் பயன்படுத்தினேன்' : 'Record Waste Diverted with this Method'),
                        ),
                      ],
                    ),
                  ),
                )),
                const SizedBox(height: 20),

                // Return / Navigate buttons
                Row(
                  children: [
                    Expanded(
                      child: OutlinedButton(
                        onPressed: () => context.go('/catalogue'),
                        child: Text(isTamil ? 'காய்கறி பட்டியல்' : 'Catalogue'),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: ElevatedButton(
                        onPressed: () => context.go('/history'),
                        child: Text(isTamil ? 'கழிவு வரலாறு' : 'Waste History'),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
