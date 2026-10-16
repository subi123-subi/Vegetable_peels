import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  bool _retainScanPhotos = true;
  double _confidenceThreshold = 0.65;

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'அமைப்புகள்' : 'Application Settings'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/profile'),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 750),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Card(
                  child: Column(
                    children: [
                      SwitchListTile(
                        title: Text(isTamil ? 'தமிழ் இடைமுகம்' : 'Tamil Interface (தமிழ்)'),
                        subtitle: Text(isTamil ? 'முழுமையான தமிழ் மொழி பயன்பாடு' : 'Switch full UI and scientific labels to Tamil'),
                        value: isTamil,
                        activeThumbColor: AppTheme.primaryGreen,
                        onChanged: (val) {
                          ref.read(localeProvider.notifier).setLanguage(val ? AppLanguage.ta : AppLanguage.en);
                        },
                      ),
                      const Divider(height: 1),
                      SwitchListTile(
                        title: Text(isTamil ? 'புகைப்படங்களைச் சேமி' : 'Retain Scanned Photographs'),
                        subtitle: Text(isTamil ? 'வரலாற்றில் உங்கள் படங்களை பாதுகாப்பாக வைத்திருக்க' : 'Keep uploaded sample images in secure local storage'),
                        value: _retainScanPhotos,
                        activeThumbColor: AppTheme.primaryGreen,
                        onChanged: (val) {
                          setState(() => _retainScanPhotos = val);
                        },
                      ),
                      const Divider(height: 1),
                      ListTile(
                        title: Text(isTamil ? 'ஏஐ நம்பிக்கை வரம்பு' : 'AI Confidence Threshold'),
                        subtitle: Text('Current: ${(_confidenceThreshold * 100).toInt()}% minimum match to accept'),
                        trailing: SizedBox(
                          width: 140,
                          child: Slider(
                            value: _confidenceThreshold,
                            min: 0.50,
                            max: 0.90,
                            divisions: 8,
                            activeColor: AppTheme.primaryGreen,
                            onChanged: (val) => setState(() => _confidenceThreshold = val),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),

                // Scientific Attribution Card
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          isTamil ? 'அறிவியல் தரவு மூலங்கள்' : 'Scientific References & Standards',
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: AppTheme.primaryDark),
                        ),
                        const SizedBox(height: 10),
                        Text(
                          '• ICMR-National Institute of Nutrition (IFCT 2017)\n'
                          '• USDA FoodData Central (FDC Standard Reference)\n'
                          '• Peer-Reviewed Food Science & Valorization Literature\n'
                          '• Google MobileNetV3 Botanical Transfer Learning Weights',
                          style: TextStyle(color: Colors.grey.shade700, fontSize: 13, height: 1.5),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 20),

                // App Info
                Center(
                  child: Column(
                    children: [
                      Text(
                        'Smart Peel AI v1.0.0 (Production Build)',
                        style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Engineered for Scientific Responsibility & Food Waste Valorization',
                        style: TextStyle(color: Colors.grey.shade500, fontSize: 11),
                      ),
                    ],
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
