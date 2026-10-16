import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';

class WelcomeScreen extends ConsumerWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: OutlinedButton.icon(
              onPressed: () {
                ref.read(localeProvider.notifier).toggleLanguage();
              },
              icon: const Icon(Icons.translate, size: 16, color: AppTheme.primaryGreen),
              label: Text(
                isTamil ? 'Switch to English' : 'தமிழ் பதிப்பு',
                style: const TextStyle(color: AppTheme.primaryGreen, fontWeight: FontWeight.bold),
              ),
              style: OutlinedButton.styleFrom(
                side: const BorderSide(color: AppTheme.primaryGreen),
              ),
            ),
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 600),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Icon(
                    Icons.eco_rounded,
                    size: 72,
                    color: AppTheme.primaryGreen,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    AppStrings.get('app_name', lang),
                    style: const TextStyle(
                      fontSize: 26,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.primaryDark,
                      letterSpacing: 1.2,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    isTamil
                        ? 'காய்கறி தோல்களை அடையாளம் கண்டு, அறிவியல் சான்றளிக்கப்பட்ட ஊட்டச்சத்துக்களை அறிந்து, கழிவுகளை உரமாக மற்றும் மறுபயன்பாட்டிற்கு மாற்றுங்கள்.'
                        : 'Transform discarded vegetable peels into verified nutritional insights, safe valorization recipes, and compost diversion.',
                    style: TextStyle(fontSize: 15, color: Colors.grey.shade700, height: 1.4),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 28),
                  // Target sectors badge row
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    alignment: WrapAlignment.center,
                    children: [
                      _buildPill(Icons.home, isTamil ? 'வீடுகள்' : 'Households'),
                      _buildPill(Icons.agriculture, isTamil ? 'விவசாயிகள்' : 'Farmers'),
                      _buildPill(Icons.storefront, isTamil ? 'சந்தைகள்' : 'Markets'),
                      _buildPill(Icons.restaurant, isTamil ? 'உணவகங்கள்' : 'Restaurants'),
                      _buildPill(Icons.science, isTamil ? 'ஆராய்ச்சியாளர்கள்' : 'Researchers'),
                    ],
                  ),
                  const SizedBox(height: 36),
                  ElevatedButton.icon(
                    onPressed: () {
                      context.go('/home');
                    },
                    icon: const Icon(Icons.bolt_rounded),
                    label: Text(isTamil ? 'உடனே தொடங்குங்கள்' : 'Start Instant Scan'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                  ),
                  const SizedBox(height: 14),
                  OutlinedButton.icon(
                    onPressed: () {
                      context.go('/catalogue');
                    },
                    icon: const Icon(Icons.menu_book),
                    label: Text(isTamil ? '50 காய்கறி பட்டியல் பார்க்க' : 'Browse 50 Vegetable Catalogue'),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                  ),
                  const SizedBox(height: 24),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        isTamil ? 'ஏற்கனவே கணக்கு உள்ளதா?' : 'Have an account? ',
                        style: TextStyle(color: Colors.grey.shade700),
                      ),
                      TextButton(
                        onPressed: () {
                          context.go('/login');
                        },
                        child: Text(
                          isTamil ? 'உள்நுழைய' : 'Sign In',
                          style: const TextStyle(fontWeight: FontWeight.bold, color: AppTheme.primaryGreen),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildPill(IconData icon, String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: AppTheme.softMint,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.green.shade200),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 14, color: AppTheme.primaryGreen),
          const SizedBox(width: 6),
          Text(
            text,
            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppTheme.primaryDark),
          ),
        ],
      ),
    );
  }
}
