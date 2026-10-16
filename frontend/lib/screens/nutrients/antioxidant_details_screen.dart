import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/nutrient_providers.dart';

class AntioxidantDetailsScreen extends ConsumerWidget {
  const AntioxidantDetailsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final bioactivesAsync = ref.watch(bioactivesAsyncProvider);
    final bioactives = bioactivesAsync.value ?? [];

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'நார்ச்சத்து & ஆன்டி-ஆக்ஸிடன்ட்கள்' : 'Dietary Fibre & Bioactive Phytochemicals'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/nutrients'),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 820),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Info Banner
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppTheme.softMint,
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.spa, color: AppTheme.primaryDark),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          isTamil
                              ? 'காய்கறி தோல்கள் புற ஊதா கதிர்களிடமிருந்து தாவரங்களை காக்கும் இயற்கை பினாலிக் சேர்மங்கள், குவர்செடின், லைகோபீன் மற்றும் பீட்டலைன்களை கொண்டுள்ளன.'
                              : 'Vegetable skins synthesize dense protective bioactives (quercetin, betalains, lycopene, and insoluble fibre) as primary barriers against UV radiation and microbial stress.',
                          style: const TextStyle(fontSize: 12, color: AppTheme.primaryDark, height: 1.3),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),

                if (bioactivesAsync.isLoading)
                  const Center(child: Padding(padding: EdgeInsets.all(32), child: CircularProgressIndicator()))
                else
                  ...bioactives.map((item) => Card(
                        elevation: 1,
                        margin: const EdgeInsets.only(bottom: 12),
                        child: Padding(
                          padding: const EdgeInsets.all(18.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  CircleAvatar(
                                    radius: 16,
                                    backgroundColor: AppTheme.softMint,
                                    child: const Icon(Icons.spa, color: AppTheme.primaryGreen, size: 18),
                                  ),
                                  const SizedBox(width: 10),
                                  Expanded(
                                    child: Text(
                                      item.displayName(isTamil),
                                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                                    ),
                                  ),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                    decoration: BoxDecoration(color: Colors.grey.shade100, borderRadius: BorderRadius.circular(6)),
                                    child: Text('Unit: ${item.standardUnit}', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 10),
                              Text(
                                item.displayRole(isTamil),
                                style: TextStyle(fontSize: 13, color: Colors.grey.shade800, height: 1.3),
                              ),
                              const SizedBox(height: 8),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                                decoration: BoxDecoration(
                                  color: AppTheme.surfaceMuted,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(
                                  'Bioactive code: ${item.code} • Non-vitamin natural phytochemical',
                                  style: TextStyle(fontSize: 11, fontStyle: FontStyle.italic, color: Colors.grey.shade700),
                                ),
                              ),
                            ],
                          ),
                        ),
                      )),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
