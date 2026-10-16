import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/nutrient_providers.dart';

class MineralDetailsScreen extends ConsumerWidget {
  const MineralDetailsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final mineralsAsync = ref.watch(mineralsAsyncProvider);
    final minerals = mineralsAsync.value ?? [];

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'தாதுக்கள் வழிகாட்டி' : 'Mineral & Electrolyte Guide (10 Essential)'),
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
                    color: Colors.blue.shade50,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: Colors.blue.shade200),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.info_outline, color: Colors.blue.shade800),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          isTamil
                              ? 'காய்கறி தோல்கள் உடலுக்கு தேவையான பொட்டாசியம், கால்சியம், இரும்புச்சத்து மற்றும் மெக்னீசியத்தை இயற்கையாக கொண்டுள்ளன.'
                              : 'Vegetable epidermal layers function as mineral storage reserves, concentrating potassium, calcium, iron, and magnesium from soil uptake.',
                          style: TextStyle(fontSize: 12, color: Colors.blue.shade900, height: 1.3),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),

                if (mineralsAsync.isLoading)
                  const Center(child: Padding(padding: EdgeInsets.all(32), child: CircularProgressIndicator()))
                else
                  ...minerals.map((min) => Card(
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
                                    backgroundColor: Colors.blue.shade100,
                                    child: Icon(Icons.grain, color: Colors.blue.shade800, size: 18),
                                  ),
                                  const SizedBox(width: 10),
                                  Expanded(
                                    child: Text(
                                      min.displayName(isTamil),
                                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                                    ),
                                  ),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                    decoration: BoxDecoration(color: Colors.grey.shade100, borderRadius: BorderRadius.circular(6)),
                                    child: Text('Unit: ${min.standardUnit}', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 10),
                              Text(
                                min.displayRole(isTamil),
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
                                  'Mineral code: ${min.code} • Standard ICP-MS / AAS Analytical Unit',
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
