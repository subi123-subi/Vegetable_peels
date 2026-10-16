import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';

class SplashScreen extends ConsumerStatefulWidget {
  const SplashScreen({super.key});

  @override
  ConsumerState<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends ConsumerState<SplashScreen> {
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _timer = Timer(const Duration(seconds: 2), () {
      if (mounted) {
        context.go('/welcome');
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);

    return Scaffold(
      backgroundColor: const Color(0xFF1B5E20), // Deep botanical forest green
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(32.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  padding: const EdgeInsets.all(28),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.12),
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.lightGreenAccent.withValues(alpha: 0.5), width: 2),
                  ),
                  child: const Icon(
                    Icons.energy_savings_leaf_rounded,
                    size: 80,
                    color: Colors.lightGreenAccent,
                  ),
                ),
                const SizedBox(height: 32),
                Text(
                  AppStrings.get('app_name', lang),
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 2.0,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 12),
                Text(
                  AppStrings.get('tagline', lang),
                  style: TextStyle(
                    color: Colors.white.withValues(alpha: 0.85),
                    fontSize: 14,
                    height: 1.4,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 48),
                const CircularProgressIndicator(
                  color: Colors.lightGreenAccent,
                  strokeWidth: 3,
                ),
                const SizedBox(height: 32),
                TextButton(
                  onPressed: () {
                    context.go('/welcome');
                  },
                  child: Text(
                    'Tap to Skip >',
                    style: TextStyle(color: Colors.white.withValues(alpha: 0.7)),
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
