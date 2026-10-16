import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';

class UserProfileScreen extends ConsumerWidget {
  const UserProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final auth = ref.watch(authProvider);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20.0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 700),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    children: [
                      CircleAvatar(
                        radius: 40,
                        backgroundColor: AppTheme.softMint,
                        child: Icon(
                          auth.isAdmin ? Icons.admin_panel_settings : Icons.person,
                          size: 48,
                          color: AppTheme.primaryGreen,
                        ),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        auth.isAuthenticated ? auth.fullName : (isTamil ? 'விருந்தினர் பயனர்' : 'Guest Account'),
                        style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                      ),
                      Text(
                        auth.isAuthenticated ? auth.email : (isTamil ? 'உள்நுழையவில்லை' : 'Not signed in'),
                        style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                      ),
                      const SizedBox(height: 12),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(
                          color: auth.isAdmin ? Colors.amber.shade100 : AppTheme.softMint,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          auth.isAdmin ? 'Role: System Administrator' : (auth.isAuthenticated ? 'Role: Registered User' : 'Role: Public Guest'),
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                            color: auth.isAdmin ? Colors.brown.shade800 : AppTheme.primaryDark,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // Account Controls
              Card(
                child: Column(
                  children: [
                    ListTile(
                      leading: const Icon(Icons.language, color: AppTheme.primaryGreen),
                      title: Text(isTamil ? 'மொழி விருப்பம்' : 'Interface Language'),
                      trailing: Text(
                        isTamil ? 'தமிழ்' : 'English',
                        style: const TextStyle(fontWeight: FontWeight.bold, color: AppTheme.primaryGreen),
                      ),
                      onTap: () {
                        ref.read(localeProvider.notifier).toggleLanguage();
                      },
                    ),
                    const Divider(height: 1),
                    ListTile(
                      leading: const Icon(Icons.settings_outlined, color: AppTheme.earthBrown),
                      title: Text(isTamil ? 'அமைப்புகள் & விருப்பத்தேர்வுகள்' : 'App Settings & Preferences'),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () => context.go('/settings'),
                    ),
                    const Divider(height: 1),
                    ListTile(
                      leading: const Icon(Icons.history, color: AppTheme.primaryGreen),
                      title: Text(isTamil ? 'எனது முந்தைய ஸ்கேன்கள்' : 'My Identification History'),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () => context.go('/history'),
                    ),
                    if (auth.isAdmin) ...[
                      const Divider(height: 1),
                      ListTile(
                        leading: const Icon(Icons.admin_panel_settings, color: Colors.orange),
                        title: Text(isTamil ? 'நிர்வாக கட்டுப்பாட்டு அறை' : 'Administrator Control Panel'),
                        trailing: const Icon(Icons.chevron_right),
                        onTap: () => context.go('/admin-dashboard'),
                      ),
                    ],
                    const Divider(height: 1),
                    ListTile(
                      leading: Icon(auth.isAuthenticated ? Icons.logout : Icons.login, color: auth.isAuthenticated ? Colors.red : AppTheme.primaryGreen),
                      title: Text(
                        auth.isAuthenticated ? (isTamil ? 'வெளியேறு' : 'Sign Out') : (isTamil ? 'உள்நுழைய' : 'Sign In with Account'),
                        style: TextStyle(color: auth.isAuthenticated ? Colors.red : AppTheme.primaryGreen, fontWeight: FontWeight.bold),
                      ),
                      onTap: () {
                        if (auth.isAuthenticated) {
                          ref.read(authProvider.notifier).logout();
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text(isTamil ? 'வெற்றிகரமாக வெளியேற்றப்பட்டீர்கள்.' : 'Signed out successfully.')),
                          );
                        } else {
                          context.go('/login');
                        }
                      },
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
}
