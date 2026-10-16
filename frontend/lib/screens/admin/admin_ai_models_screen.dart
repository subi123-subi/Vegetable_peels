import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';

class AdminAiModelsScreen extends ConsumerWidget {
  const AdminAiModelsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    final models = [
      {
        'version': 'v1.0.0-mobilenetv3',
        'arch': 'MobileNetV3Large (Transfer Learning)',
        'accuracy': '92.4%',
        'macro_f1': '0.912',
        'classes': '5 Classes: Carrot, Potato, Beetroot, Cucumber, Pumpkin peels',
        'status': 'ACTIVE PRODUCTION',
        'input_shape': '224 x 224 x 3',
        'weights': 'ai/models/smart_peel_mobilenetv3.keras',
      },
      {
        'version': 'v1.1.0-candidate',
        'arch': 'MobileNetV3Large + Gourds Expanded',
        'accuracy': '88.7%',
        'macro_f1': '0.871',
        'classes': '8 Classes: Adding Ridge Gourd, Bottle Gourd, Bitter Gourd',
        'status': 'CANDIDATE (Validation in progress)',
        'input_shape': '224 x 224 x 3',
        'weights': 'ai/models/smart_peel_v1_1_candidate.keras',
      },
    ];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF263238),
        title: Text(isTamil ? 'ஏஐ மாதிரி மேலாண்மை' : 'AI Model & Weights Management'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/admin-dashboard'),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppTheme.primaryGreen,
        icon: const Icon(Icons.upload_file, color: Colors.white),
        label: const Text('Deploy New Model Weights', style: TextStyle(color: Colors.white)),
        onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Model weights deployment dialog')),
          );
        },
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: models.length,
        itemBuilder: (context, index) {
          final m = models[index];
          final isActive = m['status']!.contains('ACTIVE');
          return Card(
            child: Padding(
              padding: const EdgeInsets.all(18.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        m['version']!,
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 17, color: AppTheme.primaryDark),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: isActive ? Colors.green.shade50 : Colors.amber.shade50,
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: isActive ? Colors.green.shade200 : Colors.amber.shade200),
                        ),
                        child: Text(
                          m['status']!,
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: isActive ? Colors.green.shade900 : Colors.amber.shade900,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text('Architecture: ${m["arch"]}', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                  Text('Input Shape: ${m["input_shape"]} • Path: ${m["weights"]}', style: TextStyle(color: Colors.grey.shade600, fontSize: 12)),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      _buildMetricBadge('Top-1 Accuracy', m['accuracy']!),
                      const SizedBox(width: 10),
                      _buildMetricBadge('Macro F1 Score', m['macro_f1']!),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(m['classes']!, style: TextStyle(fontSize: 12, color: Colors.grey.shade800)),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildMetricBadge(String label, String value) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(color: AppTheme.softMint, borderRadius: BorderRadius.circular(8)),
      child: Text(
        '$label: $value',
        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: AppTheme.primaryDark),
      ),
    );
  }
}
