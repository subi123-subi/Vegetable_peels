import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/nutrient_providers.dart';

class VitaminDetailsScreen extends ConsumerWidget {
  const VitaminDetailsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final vitaminsAsync = ref.watch(vitaminsAsyncProvider);
    final vitamins = vitaminsAsync.value ?? [];

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'வைட்டமின்கள் வழிகாட்டி' : 'Vitamin Reference Guide (13 Essential)'),
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
                // Scientific Disclaimer Card
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.amber.shade50,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: Colors.amber.shade200),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.menu_book, color: Colors.amber),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          isTamil
                              ? 'அறிவியல் குறிப்பு: வைட்டமின்கள் இருப்பது மட்டுமே ஒரு குறிப்பிட்ட தோலை உண்பதால் நோய்கள் குணமாகும் என்பதற்கான சான்றாகாது. அறிவியல் தரவு குறிப்பு மட்டுமே.'
                              : 'Scientific Notice: Nutrient presence does not claim medical cure or direct pharmacological outcome. Standard composition reference for food valorization.',
                          style: TextStyle(fontSize: 12, color: Colors.brown.shade800, height: 1.3),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),

                if (vitaminsAsync.isLoading)
                  const Center(child: Padding(padding: EdgeInsets.all(32), child: CircularProgressIndicator()))
                else
                  ...vitamins.map((vit) => Card(
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
                                    backgroundColor: Colors.orange.shade100,
                                    child: Icon(Icons.shield, color: Colors.orange.shade800, size: 18),
                                  ),
                                  const SizedBox(width: 10),
                                  Expanded(
                                    child: Text(
                                      vit.displayName(isTamil),
                                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                                    ),
                                  ),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                    decoration: BoxDecoration(color: Colors.grey.shade100, borderRadius: BorderRadius.circular(6)),
                                    child: Text('Unit: ${vit.standardUnit}', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 10),
                              Text(
                                vit.displayRole(isTamil),
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
                                  'Chemical code: ${vit.code} • Category: Essential Micronutrient',
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
