import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';

class AdminDashboardScreen extends ConsumerWidget {
  const AdminDashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    return Scaffold(
      backgroundColor: const Color(0xFFF0F4F8),
      appBar: AppBar(
        backgroundColor: const Color(0xFF263238), // Dark slate
        title: Row(
          children: [
            const Icon(Icons.admin_panel_settings, color: Colors.orange, size: 24),
            const SizedBox(width: 10),
            Text(isTamil ? 'நிர்வாக கட்டுப்பாட்டு பலகை' : 'Administrator Console'),
          ],
        ),
        actions: [
          IconButton(
            tooltip: 'Return to User View',
            icon: const Icon(Icons.exit_to_app),
            onPressed: () => context.go('/home'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 900),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Welcome Banner
                Card(
                  color: Colors.white,
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Master Management Portal',
                              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Color(0xFF263238)),
                            ),
                            Text(
                              'System-wide data validation, model versioning & audit logs',
                              style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                            ),
                          ],
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(color: Colors.green.shade50, borderRadius: BorderRadius.circular(10)),
                          child: const Text('API Online', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold, fontSize: 12)),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 20),

                // Management Modules Grid
                Text(
                  isTamil ? 'நிர்வாக தொகுதிகள்:' : 'Administrative Modules:',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF263238)),
                ),
                const SizedBox(height: 12),

                GridView.count(
                  crossAxisCount: 2,
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  crossAxisSpacing: 14,
                  mainAxisSpacing: 14,
                  childAspectRatio: 1.5,
                  children: [
                    _buildModuleTile(
                      icon: Icons.menu_book,
                      title: isTamil ? 'காய்கறி மேலாண்மை' : 'Vegetable Records',
                      subtitle: '50 Botanical records, taxonomies & hazards',
                      color: AppTheme.primaryGreen,
                      onTap: () => context.go('/admin-vegetables'),
                    ),
                    _buildModuleTile(
                      icon: Icons.science,
                      title: isTamil ? 'ஊட்டச்சத்து தரவுத்தளம்' : 'Nutrient Standards',
                      subtitle: '29 Biochemical fields, profiles & units',
                      color: Colors.blue.shade700,
                      onTap: () => context.go('/admin-nutrients'),
                    ),
                    _buildModuleTile(
                      icon: Icons.auto_stories,
                      title: isTamil ? 'அறிவியல் குறிப்புகள்' : 'Scientific Sources',
                      subtitle: 'ICMR-NIN, USDA FDC & peer-reviewed journals',
                      color: AppTheme.earthBrown,
                      onTap: () => context.go('/admin-sources'),
                    ),
                    _buildModuleTile(
                      icon: Icons.model_training,
                      title: isTamil ? 'ஏஐ மாதிரி மேலாண்மை' : 'AI Model Versions',
                      subtitle: 'MobileNetV3 deployment & class mappings',
                      color: Colors.purple.shade700,
                      onTap: () => context.go('/admin-ai-models'),
                    ),
                  ],
                ),
                const SizedBox(height: 24),

                // Audit Logs Card
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Recent Administrative Audit Logs',
                          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                        ),
                        const Divider(height: 20),
                        _buildLogItem('SEED_VEGETABLES', 'Populated 50 botanical catalogue entries', 'System'),
                        _buildLogItem('SEED_NUTRIENTS', 'Configured 29 biochemical fields (IFCT 2017)', 'System'),
                        _buildLogItem('MODEL_ACTIVATE', 'Deployed MobileNetV3Large v1.0.0 (5 classes)', 'Admin'),
                        _buildLogItem('SAFETY_CHECK', 'Initialized 4 critical safety rules', 'System'),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildModuleTile({
    required IconData icon,
    required String title,
    required String subtitle,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 2,
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircleAvatar(
                radius: 20,
                backgroundColor: color.withValues(alpha: 0.12),
                child: Icon(icon, color: color, size: 22),
              ),
              const SizedBox(height: 12),
              Text(
                title,
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
              ),
              const SizedBox(height: 4),
              Text(
                subtitle,
                style: TextStyle(color: Colors.grey.shade600, fontSize: 11),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLogItem(String action, String details, String actor) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(color: Colors.grey.shade200, borderRadius: BorderRadius.circular(4)),
                child: Text(action, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold)),
              ),
              const SizedBox(width: 10),
              Text(details, style: const TextStyle(fontSize: 12)),
            ],
          ),
          Text(actor, style: const TextStyle(fontSize: 11, color: Colors.grey)),
        ],
      ),
    );
  }
}
