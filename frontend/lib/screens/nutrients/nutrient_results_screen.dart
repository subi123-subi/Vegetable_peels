import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../models/vegetable_detail_model.dart';
import '../../providers/app_providers.dart';
import '../../providers/nutrient_providers.dart';

class NutrientResultsScreen extends ConsumerWidget {
  const NutrientResultsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final veg = ref.watch(selectedVegetableProvider);

    // Watch live scientific profile from backend
    final profileAsync = ref.watch(vegetableNutrientProfileAsyncProvider(veg.slug));
    final fallbackNutrients = ref.watch(nutrientsForSelectedVegetableProvider);

    final profile = profileAsync.value;
    final hasBackendMeasurements = profile != null && profile.measurements.isNotEmpty;

    // Categorized measurements
    final List<NutrientDetailItem> vitamins = hasBackendMeasurements
        ? profile.measurements.where((m) => m.category == 'vitamin').toList()
        : fallbackNutrients
            .where((n) => n.category == 'vitamin')
            .map((n) => NutrientDetailItem(
                  nutrientId: 0,
                  nutrientCode: n.code,
                  nutrientNameEn: n.nameEn,
                  nutrientNameTa: n.nameTa,
                  category: n.category,
                  concentrationPer100g: n.concentrationPer100g,
                  unit: n.unit,
                  biologicalRoleEn: n.biologicalRoleEn,
                  biologicalRoleTa: n.biologicalRoleTa,
                ))
            .toList();

    final List<NutrientDetailItem> minerals = hasBackendMeasurements
        ? profile.measurements.where((m) => m.category == 'mineral').toList()
        : fallbackNutrients
            .where((n) => n.category == 'mineral')
            .map((n) => NutrientDetailItem(
                  nutrientId: 0,
                  nutrientCode: n.code,
                  nutrientNameEn: n.nameEn,
                  nutrientNameTa: n.nameTa,
                  category: n.category,
                  concentrationPer100g: n.concentrationPer100g,
                  unit: n.unit,
                  biologicalRoleEn: n.biologicalRoleEn,
                  biologicalRoleTa: n.biologicalRoleTa,
                ))
            .toList();

    final List<NutrientDetailItem> others = hasBackendMeasurements
        ? profile.measurements.where((m) => m.category == 'other').toList()
        : fallbackNutrients
            .where((n) => n.category == 'other')
            .map((n) => NutrientDetailItem(
                  nutrientId: 0,
                  nutrientCode: n.code,
                  nutrientNameEn: n.nameEn,
                  nutrientNameTa: n.nameTa,
                  category: n.category,
                  concentrationPer100g: n.concentrationPer100g,
                  unit: n.unit,
                  biologicalRoleEn: n.biologicalRoleEn,
                  biologicalRoleTa: n.biologicalRoleTa,
                ))
            .toList();

    final isDryBasis = profile?.freshOrDryBasis == 'dry_weight';
    final dataStatus = profile?.dataQualityStatus ?? 'validated_peel_measurement';

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20.0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 880),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Header Summary Card
              Card(
                elevation: 1.5,
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
                              '${veg.scientificName} • ${veg.plantPart} • 100g ${isDryBasis ? "Dry" : "Fresh"} Weight Basis',
                              style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                            ),
                            const SizedBox(height: 6),
                            Wrap(
                              spacing: 8,
                              runSpacing: 4,
                              children: [
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                  decoration: BoxDecoration(
                                    color: AppTheme.softMint,
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Text(
                                    dataStatus == 'validated_peel_measurement'
                                        ? (isTamil ? 'சரிபார்க்கப்பட்ட அளவீடு (IFCT/USDA)' : 'Validated Peel Profile (IFCT 2017 & USDA)')
                                        : (isTamil ? 'குறிப்பீட்டு மதிப்பீடு' : 'Indicative Botanical Estimate'),
                                    style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: AppTheme.primaryDark),
                                  ),
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                  decoration: BoxDecoration(
                                    color: Colors.blue.shade50,
                                    borderRadius: BorderRadius.circular(8),
                                    border: Border.all(color: Colors.blue.shade200, width: 0.8),
                                  ),
                                  child: Text(
                                    isDryBasis ? 'Dry Weight Basis' : 'Fresh Weight Basis',
                                    style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: Colors.blue.shade800),
                                  ),
                                ),
                              ],
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
                    style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen, foregroundColor: Colors.white),
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
              const SizedBox(height: 20),

              // Scientific Citation Card
              if (profile?.source != null)
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.grey.shade50,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.grey.shade300),
                  ),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.menu_book_outlined, size: 20, color: AppTheme.primaryDark),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              isTamil ? 'அறிவியல் ஆதாரம் (Scientific Reference)' : 'Scientific Source Citation',
                              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: AppTheme.primaryDark),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              '${profile!.source!.title} (${profile.source!.publicationYear ?? 2022}). ${profile.source!.authors ?? ""}. ${profile.source!.journalOrPublisher ?? ""}.',
                              style: TextStyle(fontSize: 11, color: Colors.grey.shade700, height: 1.3),
                            ),
                            if (profile.samplePrepMethod != null) ...[
                              const SizedBox(height: 4),
                              Text(
                                'Method: ${profile.samplePrepMethod}',
                                style: TextStyle(fontSize: 11, fontStyle: FontStyle.italic, color: Colors.grey.shade600),
                              ),
                            ],
                          ],
                        ),
                      ),
                    ],
                  ),
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
    required List<NutrientDetailItem> items,
    required bool isTamil,
    required VoidCallback onExplore,
  }) {
    return Card(
      elevation: 1,
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Row(
                    children: [
                      CircleAvatar(
                        radius: 18,
                        backgroundColor: color.withValues(alpha: 0.12),
                        child: Icon(icon, color: color, size: 20),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(title, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold), maxLines: 1, overflow: TextOverflow.ellipsis),
                            Text(subtitle, style: TextStyle(color: Colors.grey.shade600, fontSize: 12), maxLines: 1, overflow: TextOverflow.ellipsis),
                          ],
                        ),
                      ),
                    ],
                  ),
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
                                Text(
                                  nut.displayRole(isTamil),
                                  style: TextStyle(color: Colors.grey.shade600, fontSize: 11),
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 10),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
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
                            if (nut.dataQualityStatus != null)
                              Padding(
                                padding: const EdgeInsets.only(top: 2.0),
                                child: Text(
                                  nut.dataQualityStatus!,
                                  style: TextStyle(fontSize: 9, color: Colors.grey.shade500),
                                ),
                              ),
                          ],
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
