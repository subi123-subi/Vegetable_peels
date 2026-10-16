import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';

class RegisterScreen extends ConsumerStatefulWidget {
  const RegisterScreen({super.key});

  @override
  ConsumerState<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends ConsumerState<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleRegister() {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);
      Future.delayed(const Duration(milliseconds: 600), () {
        ref.read(authProvider.notifier).login(
          _emailController.text.trim(),
          _nameController.text.trim(),
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
        title: Text(isTamil ? 'புதிய பதிவு' : 'Create Account'),
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
                        child: Icon(Icons.person_add_rounded, size: 54, color: AppTheme.primaryGreen),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        isTamil ? 'புதிய பயனர் கணக்கு' : 'Join Smart Peel AI',
                        style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        isTamil ? 'வீட்டு மற்றும் தொழில்முறை கழிவு மேலாண்மை' : 'Sustainable nutrient and waste valorization',
                        style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 28),
                      TextFormField(
                        controller: _nameController,
                        decoration: InputDecoration(
                          labelText: isTamil ? 'முழு பெயர்' : 'Full Name',
                          prefixIcon: const Icon(Icons.badge_outlined),
                        ),
                        validator: (v) => v == null || v.isEmpty ? 'Please enter your name' : null,
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _emailController,
                        decoration: InputDecoration(
                          labelText: isTamil ? 'மின்னஞ்சல்' : 'Email Address',
                          prefixIcon: const Icon(Icons.email_outlined),
                        ),
                        validator: (v) => v == null || !v.contains('@') ? 'Enter a valid email' : null,
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _passwordController,
                        obscureText: true,
                        decoration: InputDecoration(
                          labelText: isTamil ? 'கடவுச்சொல்' : 'Password',
                          prefixIcon: const Icon(Icons.lock_outline),
                        ),
                        validator: (v) => v == null || v.length < 6 ? 'Password must be at least 6 characters' : null,
                      ),
                      const SizedBox(height: 24),
                      ElevatedButton(
                        onPressed: _isLoading ? null : _handleRegister,
                        child: _isLoading
                            ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                            : Text(isTamil ? 'கணக்கை உருவாக்கு' : 'Create Account'),
                      ),
                      const SizedBox(height: 16),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(isTamil ? 'ஏற்கனவே கணக்கு உள்ளதா? ' : 'Already registered? '),
                          TextButton(
                            onPressed: () => context.go('/login'),
                            child: Text(isTamil ? 'உள்நுழைக' : 'Sign In', style: const TextStyle(fontWeight: FontWeight.bold)),
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
