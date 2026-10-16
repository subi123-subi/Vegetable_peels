import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController(text: 'user@smartpeel.ai');
  final _passwordController = TextEditingController(text: 'User@12345');
  bool _obscurePassword = true;
  bool _isLoading = false;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);
      Future.delayed(const Duration(milliseconds: 600), () {
        ref.read(authProvider.notifier).login(
          _emailController.text.trim(),
          _emailController.text.split('@').first.toUpperCase(),
          false,
        );
        if (!mounted) return;
        setState(() => _isLoading = false);
        context.go('/home');
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'உள்நுழைய' : 'User Sign In'),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 450),
            child: Card(
              child: Padding(
                padding: const EdgeInsets.all(28.0),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      const Center(
                        child: Icon(Icons.lock_person_rounded, size: 54, color: AppTheme.primaryGreen),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        isTamil ? 'உங்கள் கணக்கில் உள்நுழையவும்' : 'Welcome Back',
                        style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        isTamil ? 'சேமிக்கப்பட்ட முடிவுகளைப் பார்வையிட' : 'Access your scan history and reports',
                        style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 28),
                      TextFormField(
                        controller: _emailController,
                        decoration: InputDecoration(
                          labelText: isTamil ? 'மின்னஞ்சல்' : 'Email Address',
                          prefixIcon: const Icon(Icons.email_outlined),
                        ),
                        validator: (v) => v == null || v.isEmpty ? 'Please enter your email' : null,
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _passwordController,
                        obscureText: _obscurePassword,
                        decoration: InputDecoration(
                          labelText: isTamil ? 'கடவுச்சொல்' : 'Password',
                          prefixIcon: const Icon(Icons.lock_outline),
                          suffixIcon: IconButton(
                            icon: Icon(_obscurePassword ? Icons.visibility : Icons.visibility_off),
                            onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                          ),
                        ),
                        validator: (v) => v == null || v.length < 5 ? 'Password too short' : null,
                      ),
                      const SizedBox(height: 24),
                      ElevatedButton(
                        onPressed: _isLoading ? null : _handleLogin,
                        child: _isLoading
                            ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                            : Text(isTamil ? 'உள்நுழை' : 'Sign In'),
                      ),
                      const SizedBox(height: 12),
                      OutlinedButton(
                        onPressed: () {
                          // Continue as guest
                          ref.read(authProvider.notifier).logout();
                          context.go('/home');
                        },
                        child: Text(isTamil ? 'விருந்தினராக தொடர' : 'Continue as Guest'),
                      ),
                      const SizedBox(height: 20),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(isTamil ? 'கணக்கு இல்லையா? ' : 'No account? '),
                          TextButton(
                            onPressed: () => context.go('/register'),
                            child: Text(isTamil ? 'பதிவு செய்க' : 'Register Here', style: const TextStyle(fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
