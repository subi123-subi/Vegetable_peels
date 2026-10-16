import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../core/localization/app_locale.dart';
import '../core/theme/app_theme.dart';
import '../providers/app_providers.dart';

class AppShell extends ConsumerWidget {
  final Widget child;
  final String currentRoute;

  const AppShell({
    super.key,
    required this.child,
    required this.currentRoute,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final auth = ref.watch(authProvider);

    int selectedIndex = _calculateSelectedIndex(currentRoute);

    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            const Icon(Icons.eco_rounded, color: Colors.lightGreenAccent, size: 26),
            const SizedBox(width: 10),
            Text(
              AppStrings.get('app_name', lang),
              style: const TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1.1),
            ),
          ],
        ),
        actions: [
          // Language Switcher Button
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: OutlinedButton.icon(
              onPressed: () {
                ref.read(localeProvider.notifier).toggleLanguage();
              },
              icon: const Icon(Icons.translate, size: 16, color: Colors.white),
              label: Text(
                isTamil ? 'English' : 'தமிழ்',
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
              ),
              style: OutlinedButton.styleFrom(
                side: const BorderSide(color: Colors.white54),
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                backgroundColor: Colors.white.withValues(alpha: 0.15),
              ),
            ),
          ),
          // User / Admin status icon
          IconButton(
            tooltip: auth.isAuthenticated ? auth.fullName : 'Profile',
            icon: CircleAvatar(
              radius: 14,
              backgroundColor: auth.isAdmin ? Colors.amber.shade700 : Colors.white24,
              child: Icon(
                auth.isAdmin ? Icons.admin_panel_settings : Icons.person,
                size: 16,
                color: Colors.white,
              ),
            ),
            onPressed: () {
              if (auth.isAdmin) {
                context.go('/admin-dashboard');
              } else {
                context.go('/profile');
              }
            },
          ),
          const SizedBox(width: 8),
        ],
      ),
      drawer: Drawer(
        backgroundColor: Colors.white,
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: const BoxDecoration(
                color: AppTheme.primaryGreen,
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  const Icon(Icons.energy_savings_leaf_rounded, size: 42, color: Colors.lightGreenAccent),
                  const SizedBox(height: 10),
                  Text(
                    AppStrings.get('app_name', lang),
                    style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  Text(
                    auth.isAuthenticated ? '${auth.fullName} (${auth.isAdmin ? "Admin" : "User"})' : 'Guest Mode',
                    style: TextStyle(color: Colors.white.withValues(alpha: 0.85), fontSize: 13),
                  ),
                ],
              ),
            ),
            ListTile(
              leading: const Icon(Icons.dashboard_rounded, color: AppTheme.primaryGreen),
              title: Text(AppStrings.get('home', lang)),
              selected: currentRoute == '/home',
              onTap: () {
                Navigator.pop(context);
                context.go('/home');
              },
            ),
            ListTile(
              leading: const Icon(Icons.camera_alt_rounded, color: AppTheme.primaryGreen),
              title: Text(AppStrings.get('scan', lang)),
              selected: currentRoute == '/camera-scan',
              onTap: () {
                Navigator.pop(context);
                context.go('/camera-scan');
              },
            ),
            ListTile(
              leading: const Icon(Icons.menu_book_rounded, color: AppTheme.primaryGreen),
              title: Text(AppStrings.get('catalogue', lang)),
              selected: currentRoute == '/catalogue',
              onTap: () {
                Navigator.pop(context);
                context.go('/catalogue');
              },
            ),
            ListTile(
              leading: const Icon(Icons.history_rounded, color: AppTheme.primaryGreen),
              title: Text(AppStrings.get('history', lang)),
              selected: currentRoute == '/history',
              onTap: () {
                Navigator.pop(context);
                context.go('/history');
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.settings_rounded, color: AppTheme.earthBrown),
              title: Text(AppStrings.get('settings', lang)),
              onTap: () {
                Navigator.pop(context);
                context.go('/settings');
              },
            ),
            ListTile(
              leading: const Icon(Icons.admin_panel_settings_rounded, color: Colors.orange),
              title: Text(AppStrings.get('admin', lang)),
              onTap: () {
                Navigator.pop(context);
                if (auth.isAdmin) {
                  context.go('/admin-dashboard');
                } else {
                  context.go('/admin-login');
                }
              },
            ),
          ],
        ),
      ),
      body: child,
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex,
        backgroundColor: Colors.white,
        elevation: 3,
        indicatorColor: AppTheme.softMint,
        onDestinationSelected: (index) {
          switch (index) {
            case 0:
              context.go('/home');
              break;
            case 1:
              context.go('/camera-scan');
              break;
            case 2:
              context.go('/catalogue');
              break;
            case 3:
              context.go('/history');
              break;
            case 4:
              context.go('/profile');
              break;
          }
        },
        destinations: [
          NavigationDestination(
            icon: const Icon(Icons.dashboard_outlined),
            selectedIcon: const Icon(Icons.dashboard, color: AppTheme.primaryGreen),
            label: AppStrings.get('home', lang),
          ),
          NavigationDestination(
            icon: const Icon(Icons.camera_alt_outlined),
            selectedIcon: const Icon(Icons.camera_alt, color: AppTheme.primaryGreen),
            label: AppStrings.get('scan', lang),
          ),
          NavigationDestination(
            icon: const Icon(Icons.menu_book_outlined),
            selectedIcon: const Icon(Icons.menu_book, color: AppTheme.primaryGreen),
            label: AppStrings.get('catalogue', lang),
          ),
          NavigationDestination(
            icon: const Icon(Icons.history_outlined),
            selectedIcon: const Icon(Icons.history, color: AppTheme.primaryGreen),
            label: AppStrings.get('history', lang),
          ),
          NavigationDestination(
            icon: const Icon(Icons.person_outline),
            selectedIcon: const Icon(Icons.person, color: AppTheme.primaryGreen),
            label: AppStrings.get('profile', lang),
          ),
        ],
      ),
    );
  }

  int _calculateSelectedIndex(String route) {
    if (route.startsWith('/camera-scan') || route.startsWith('/image-upload') || route.startsWith('/identification')) {
      return 1;
    }
    if (route.startsWith('/catalogue') || route.startsWith('/search')) {
      return 2;
    }
    if (route.startsWith('/history') || route.startsWith('/report')) {
      return 3;
    }
    if (route.startsWith('/profile') || route.startsWith('/settings')) {
      return 4;
    }
    return 0; // default Home
  }
}
