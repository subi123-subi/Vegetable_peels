import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';

class HomeDashboardScreen extends ConsumerWidget {
  const HomeDashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final recentScans = ref.watch(scanHistoryProvider);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20.0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 900),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Hero Banner Card
              Container(
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [AppTheme.primaryDark, AppTheme.primaryGreen],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [
                    BoxShadow(
                      color: AppTheme.primaryGreen.withValues(alpha: 0.3),
                      blurRadius: 12,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
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
                            color: Colors.white24,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Row(
                            children: [
                              const Icon(Icons.verified_outlined, color: Colors.lightGreenAccent, size: 16),
                              const SizedBox(width: 6),
                              Text(
                                isTamil ? 'அறிவியல் முறைமை v1.0' : 'Scientific Framework v1.0',
                                style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
                              ),
                            ],
                          ),
                        ),
                        IconButton(
                          onPressed: () => context.go('/search'),
                          icon: const Icon(Icons.search, color: Colors.white),
                          tooltip: 'Search',
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Text(
                      isTamil ? 'காய்கறி தோல்களை அடையாளம் காணுங்கள்' : 'Identify Vegetable Peels with AI',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      isTamil
                          ? 'சான்றளிக்கப்பட்ட ஊட்டச்சத்து மதிப்புகள் மற்றும் பாதுகாப்பான பயன்பாட்டு ஆலோசனைகளைப் பெறுங்கள்.'
                          : 'Get referenced micronutrient compositions, food safety checks, and valorization methods.',
                      style: TextStyle(color: Colors.white.withValues(alpha: 0.9), fontSize: 14),
                    ),
                    const SizedBox(height: 20),
                    Wrap(
                      spacing: 12,
                      runSpacing: 10,
                      children: [
                        ElevatedButton.icon(
                          onPressed: () => context.go('/camera-scan'),
                          icon: const Icon(Icons.camera_alt, color: AppTheme.primaryDark),
                          label: Text(
                            isTamil ? 'தோல் ஸ்கேன்' : 'Live Camera Scan',
                            style: const TextStyle(color: AppTheme.primaryDark, fontWeight: FontWeight.bold),
                          ),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                          ),
                        ),
                        OutlinedButton.icon(
                          onPressed: () => context.go('/image-upload'),
                          icon: const Icon(Icons.file_upload_outlined, color: Colors.white),
                          label: Text(
                            isTamil ? 'படம் பதிவேற்றம்' : 'Upload Image',
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                          ),
                          style: OutlinedButton.styleFrom(
                            side: const BorderSide(color: Colors.white70),
                            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // KPI Impact Metrics Row
              Wrap(
                spacing: 14,
                runSpacing: 14,
                children: [
                  _buildMetricTile(
                    icon: Icons.grass,
                    title: isTamil ? 'ஆதரிக்கப்படும் காய்கறிகள்' : 'Botanical Catalogue',
                    value: '50 Types',
                    color: AppTheme.primaryGreen,
                  ),
                  _buildMetricTile(
                    icon: Icons.recycling_rounded,
                    title: isTamil ? 'பதிவுசெய்த கழிவு திசைதிருப்பல்' : 'Tracked Waste Diversion',
                    value: '14.2 kg',
                    color: AppTheme.leafGreen,
                  ),
                  _buildMetricTile(
                    icon: Icons.science_outlined,
                    title: isTamil ? 'ஊட்டச்சத்து கூறுகள்' : 'Scientific Nutrients',
                    value: '29 Fields',
                    color: AppTheme.nutritionCyan,
                  ),
                  _buildMetricTile(
                    icon: Icons.gpp_good_outlined,
                    title: isTamil ? 'பாதுகாப்பு விதிகள்' : 'Food Safety Engine',
                    value: 'Active',
                    color: Colors.orange.shade800,
                  ),
                ],
              ),
              const SizedBox(height: 28),

              // Scientific Integrity Disclaimer Box
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFFFFF8E1),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: const Color(0xFFFFE082)),
                ),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.info_outline_rounded, color: Color(0xFFF57F17), size: 22),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            isTamil ? 'அறிவியல் வெளிப்படைத்தன்மை' : 'Scientific Transparency Notice',
                            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFFF57F17)),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            AppStrings.get('scientific_disclaimer', lang),
                            style: TextStyle(color: Colors.brown.shade800, fontSize: 12, height: 1.3),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 28),

              // Section Header: Recent Identification Records
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    isTamil ? 'சமீபத்திய ஸ்கேன்கள்' : 'Recent Scan Sessions',
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppTheme.earthDark),
                  ),
                  TextButton.icon(
                    onPressed: () => context.go('/history'),
                    icon: const Icon(Icons.arrow_forward, size: 16),
                    label: Text(isTamil ? 'அனைத்தும்' : 'View All'),
                  ),
                ],
              ),
              const SizedBox(height: 8),

              // Recent Scans List
              if (recentScans.isEmpty)
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Center(
                      child: Text(
                        isTamil ? 'இன்னும் ஸ்கேன்கள் எதுவும் இல்லை. ஒரு புகைப்படத்தை எடுக்கவும்!' : 'No scans recorded yet. Capture or upload a peel to get started!',
                        style: TextStyle(color: Colors.grey.shade600),
                      ),
                    ),
                  ),
                )
              else
                ...recentScans.map((scan) => Card(
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: AppTheme.softMint,
                      child: const Icon(Icons.eco, color: AppTheme.primaryGreen),
                    ),
                    title: Text(
                      scan.predictedVegetable.displayName(isTamil),
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(
                      '${scan.predictedVegetable.scientificName} • ${(scan.confidence * 100).toStringAsFixed(1)}% AI Confidence',
                    ),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () {
                      ref.read(selectedVegetableProvider.notifier).select(scan.predictedVegetable);
                      context.go('/nutrients');
                    },
                  ),
                )),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMetricTile({
    required IconData icon,
    required String title,
    required String value,
    required Color color,
  }) {
    return Container(
      width: 195,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey.shade200),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.02),
            blurRadius: 6,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CircleAvatar(
            radius: 18,
            backgroundColor: color.withValues(alpha: 0.12),
            child: Icon(icon, color: color, size: 20),
          ),
          const SizedBox(height: 12),
          Text(
            value,
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color),
          ),
          const SizedBox(height: 4),
          Text(
            title,
            style: TextStyle(fontSize: 12, color: Colors.grey.shade600, fontWeight: FontWeight.w500),
          ),
        ],
      ),
    );
  }
}
