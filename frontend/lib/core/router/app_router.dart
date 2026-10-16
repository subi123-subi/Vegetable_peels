import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../widgets/app_shell.dart';
import '../../screens/splash/splash_screen.dart';
import '../../screens/auth/welcome_screen.dart';
import '../../screens/auth/login_screen.dart';
import '../../screens/auth/register_screen.dart';
import '../../screens/home/home_dashboard_screen.dart';
import '../../screens/scan/camera_scan_screen.dart';
import '../../screens/scan/image_upload_screen.dart';
import '../../screens/scan/vegetable_identification_screen.dart';
import '../../screens/nutrients/nutrient_results_screen.dart';
import '../../screens/nutrients/vitamin_details_screen.dart';
import '../../screens/nutrients/mineral_details_screen.dart';
import '../../screens/nutrients/antioxidant_details_screen.dart';
import '../../screens/nutrients/nutrient_estimation_screen.dart';
import '../../screens/safety/safety_information_screen.dart';
import '../../screens/reuse/waste_reuse_screen.dart';
import '../../screens/catalogue/vegetable_catalogue_screen.dart';
import '../../screens/catalogue/search_screen.dart';
import '../../screens/history/scan_history_screen.dart';
import '../../screens/reports/report_download_screen.dart';
import '../../screens/profile/user_profile_screen.dart';
import '../../screens/settings/settings_screen.dart';
import '../../screens/admin/admin_login_screen.dart';
import '../../screens/admin/admin_dashboard_screen.dart';
import '../../screens/admin/admin_vegetables_screen.dart';
import '../../screens/admin/admin_nutrients_screen.dart';
import '../../screens/admin/admin_sources_screen.dart';
import '../../screens/admin/admin_ai_models_screen.dart';

final GlobalKey<NavigatorState> _rootNavigatorKey = GlobalKey<NavigatorState>();
final GlobalKey<NavigatorState> _shellNavigatorKey = GlobalKey<NavigatorState>();

final appRouter = GoRouter(
  navigatorKey: _rootNavigatorKey,
  initialLocation: '/',
  routes: [
    // Screen 1: Splash
    GoRoute(
      path: '/',
      builder: (context, state) => const SplashScreen(),
    ),
    // Screen 2: Welcome
    GoRoute(
      path: '/welcome',
      builder: (context, state) => const WelcomeScreen(),
    ),
    // Screen 3: Login
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
    // Screen 4: Registration
    GoRoute(
      path: '/register',
      builder: (context, state) => const RegisterScreen(),
    ),
    // Screen 22: Admin Login
    GoRoute(
      path: '/admin-login',
      builder: (context, state) => const AdminLoginScreen(),
    ),
    // Screen 23: Admin Dashboard
    GoRoute(
      path: '/admin-dashboard',
      builder: (context, state) => const AdminDashboardScreen(),
    ),
    // Screen 24: Admin Vegetables
    GoRoute(
      path: '/admin-vegetables',
      builder: (context, state) => const AdminVegetablesScreen(),
    ),
    // Screen 25: Admin Nutrients
    GoRoute(
      path: '/admin-nutrients',
      builder: (context, state) => const AdminNutrientsScreen(),
    ),
    // Screen 26: Admin Sources
    GoRoute(
      path: '/admin-sources',
      builder: (context, state) => const AdminSourcesScreen(),
    ),
    // Screen 27: Admin AI Models
    GoRoute(
      path: '/admin-ai-models',
      builder: (context, state) => const AdminAiModelsScreen(),
    ),
    // Screen 10: Vitamin Details
    GoRoute(
      path: '/vitamin-details',
      builder: (context, state) => const VitaminDetailsScreen(),
    ),
    // Screen 11: Mineral Details
    GoRoute(
      path: '/mineral-details',
      builder: (context, state) => const MineralDetailsScreen(),
    ),
    // Screen 12: Antioxidant Details
    GoRoute(
      path: '/antioxidant-details',
      builder: (context, state) => const AntioxidantDetailsScreen(),
    ),
    // Screen 13: Nutrient Estimation
    GoRoute(
      path: '/nutrient-estimation',
      builder: (context, state) => const NutrientEstimationScreen(),
    ),
    // Screen 14: Safety Information
    GoRoute(
      path: '/safety-info',
      builder: (context, state) => const SafetyInformationScreen(),
    ),
    // Screen 15: Waste Reuse
    GoRoute(
      path: '/waste-reuse',
      builder: (context, state) => const WasteReuseScreen(),
    ),
    // Screen 17: Search Screen
    GoRoute(
      path: '/search',
      builder: (context, state) => const SearchScreen(),
    ),
    // Screen 19: Report Download
    GoRoute(
      path: '/report-download',
      builder: (context, state) => const ReportDownloadScreen(),
    ),
    // Screen 21: Settings Screen
    GoRoute(
      path: '/settings',
      builder: (context, state) => const SettingsScreen(),
    ),

    // Shell Route for persistent Navigation Bar & Drawer
    ShellRoute(
      navigatorKey: _shellNavigatorKey,
      builder: (context, state, child) {
        return AppShell(
          currentRoute: state.uri.path,
          child: child,
        );
      },
      routes: [
        // Screen 5: Home Dashboard
        GoRoute(
          path: '/home',
          builder: (context, state) => const HomeDashboardScreen(),
        ),
        // Screen 6: Camera Scan
        GoRoute(
          path: '/camera-scan',
          builder: (context, state) => const CameraScanScreen(),
        ),
        // Screen 7: Image Upload
        GoRoute(
          path: '/image-upload',
          builder: (context, state) => const ImageUploadScreen(),
        ),
        // Screen 8: Vegetable Identification
        GoRoute(
          path: '/identification',
          builder: (context, state) => const VegetableIdentificationScreen(),
        ),
        // Screen 9: Nutrient Results
        GoRoute(
          path: '/nutrients',
          builder: (context, state) => const NutrientResultsScreen(),
        ),
        // Screen 16: Vegetable Catalogue
        GoRoute(
          path: '/catalogue',
          builder: (context, state) => const VegetableCatalogueScreen(),
        ),
        // Screen 18: Scan History
        GoRoute(
          path: '/history',
          builder: (context, state) => const ScanHistoryScreen(),
        ),
        // Screen 20: User Profile
        GoRoute(
          path: '/profile',
          builder: (context, state) => const UserProfileScreen(),
        ),
      ],
    ),
  ],
);
