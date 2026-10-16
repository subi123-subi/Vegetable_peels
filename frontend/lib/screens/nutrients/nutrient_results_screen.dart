import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../models/app_models.dart';
import '../../providers/app_providers.dart';

class NutrientResultsScreen extends ConsumerWidget {
  const NutrientResultsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final veg = ref.watch(selectedVegetableProvider);
    final nutrients = ref.watch(nutrientsForSelectedVegetableProvider);

    final vitamins = nutrients.where((n) => n.category == 'vitamin').toList();
    final minerals = nutrients.where((n) => n.category == 'mineral').toList();
    final others = nutrients.where((n) => n.category == 'other').toList();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20.0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 850),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Header Summary Card
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Row(
                    children: [
                      CircleAvatar(
                        radius: 28,
                        backgroundColor: AppTheme.softMint,
                        child: const Icon(Icons.eco, color: AppTheme.primaryGreen, size: 32),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              veg.displayName(isTamil),
                              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                            ),
                            Text(
                              '${veg.scientificName} • ${veg.plantPart} • 100g Fresh Weight Basis',
                              style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                            ),
                            const SizedBox(height: 6),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                              decoration: BoxDecoration(
                                color: AppTheme.softMint,
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                isTamil ? 'தரவு நிலை: சரிபார்க்கப்பட்ட அளவீடு' : 'Data Status: Validated Peel Profile (IFCT/USDA)',
                                style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: AppTheme.primaryDark),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 16),

              // Action Toolbar
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children: [
                  ElevatedButton.icon(
                    onPressed: () => context.go('/nutrient-estimation'),
                    icon: const Icon(Icons.calculate_outlined),
                    label: Text(isTamil ? 'எடை மூலம் கணக்கிடுக' : 'Estimate by Peel Weight'),
                  ),
                  OutlinedButton.icon(
                    onPressed: () => context.go('/safety-info'),
                    icon: const Icon(Icons.security, color: Colors.orange),
                    label: Text(
                      isTamil ? 'பாதுகாப்பு எச்சரிக்கைகள்' : 'Safety Alerts',
                      style: const TextStyle(color: Colors.orange),
                    ),
                  ),
                  OutlinedButton.icon(
                    onPressed: () => context.go('/waste-reuse'),
                    icon: const Icon(Icons.recycling, color: AppTheme.primaryGreen),
                    label: Text(
                      isTamil ? 'மறுபயன்பாட்டு முறைகள்' : 'Valorization Methods',
                      style: const TextStyle(color: AppTheme.primaryGreen),
                    ),
                  ),
                  OutlinedButton.icon(
                    onPressed: () => context.go('/report-download'),
                    icon: const Icon(Icons.picture_as_pdf, color: Colors.blueGrey),
                    label: Text(
                      isTamil ? 'அறிக்கை' : 'Report',
                      style: const TextStyle(color: Colors.blueGrey),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // Category Cards
              _buildCategoryCard(
                context: context,
                title: isTamil ? 'வைட்டமின்கள்' : 'Vitamins',
                subtitle: isTamil ? 'முக்கிய உயிர்ச்சத்துக்கள் மற்றும் உடலியல் பங்கு' : 'Essential micronutrients and metabolic roles',
                icon: Icons.shield_outlined,
                color: Colors.orange.shade800,
                items: vitamins,
                isTamil: isTamil,
                onExplore: () => context.go('/vitamin-details'),
              ),
              const SizedBox(height: 16),

              _buildCategoryCard(
                context: context,
                title: isTamil ? 'தாதுக்கள் (மினரல்கள்)' : 'Minerals & Electrolytes',
                subtitle: isTamil ? 'எலும்பு, தசை மற்றும் நொதி இயக்கங்கள்' : 'Enzymatic cofactors and structural ions',
                icon: Icons.grain_outlined,
                color: Colors.blue.shade800,
                items: minerals,
                isTamil: isTamil,
                onExplore: () => context.go('/mineral-details'),
              ),
              const SizedBox(height: 16),

              _buildCategoryCard(
                context: context,
                title: isTamil ? 'நார்ச்சத்து மற்றும் ஆன்டி-ஆக்ஸிடன்ட்கள்' : 'Dietary Fibre & Bioactives',
                subtitle: isTamil ? 'செரிமான நார்ச்சத்து மற்றும் தாவர வேதிப்பொருட்கள்' : 'Colonic motility fibres and free-radical scavengers',
                icon: Icons.spa_outlined,
                color: AppTheme.primaryGreen,
                items: others,
                isTamil: isTamil,
                onExplore: () => context.go('/antioxidant-details'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCategoryCard({
    required BuildContext context,
    required String title,
    required String subtitle,
    required IconData icon,
    required Color color,
    required List<NutrientItem> items,
    required bool isTamil,
    required VoidCallback onExplore,
  }) {
    return Card(
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
                      radius: 18,
                      backgroundColor: color.withValues(alpha: 0.12),
                      child: Icon(icon, color: color, size: 20),
                    ),
                    const SizedBox(width: 12),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(title, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
                        Text(subtitle, style: TextStyle(color: Colors.grey.shade600, fontSize: 12)),
                      ],
                    ),
                  ],
                ),
                TextButton(
                  onPressed: onExplore,
                  child: Text(isTamil ? 'விவரங்கள் >' : 'Deep Dive >'),
                ),
              ],
            ),
            const Divider(height: 24),
            if (items.isEmpty)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8.0),
                child: Text(
                  isTamil ? 'குறிப்பிட்ட அளவீட்டு தரவு கிடைக்கவில்லை.' : 'Peel-specific measurement unavailable in reference literature.',
                  style: TextStyle(color: Colors.grey.shade600, fontStyle: FontStyle.italic),
                ),
              )
            else
              ...items.map((nut) => Padding(
                padding: const EdgeInsets.symmetric(vertical: 6.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(nut.displayName(isTamil), style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                          if (nut.displayRole(isTamil).isNotEmpty)
                            Text(nut.displayRole(isTamil), style: TextStyle(color: Colors.grey.shade600, fontSize: 11), maxLines: 1, overflow: TextOverflow.ellipsis),
                        ],
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.grey.shade100,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        '${nut.concentrationPer100g} ${nut.unit}',
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                      ),
                    ),
                  ],
                ),
              )),
          ],
        ),
      ),
    );
  }
}
