import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../providers/app_providers.dart';

class AdminLoginScreen extends ConsumerStatefulWidget {
  const AdminLoginScreen({super.key});

  @override
  ConsumerState<AdminLoginScreen> createState() => _AdminLoginScreenState();
}

class _AdminLoginScreenState extends ConsumerState<AdminLoginScreen> {
  final _emailController = TextEditingController(text: 'admin@smartpeel.ai');
  final _passwordController = TextEditingController(text: 'Admin@SmartPeel2026!');
  bool _isLoading = false;
  String? _errorMessage;

  void _handleAdminLogin() {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    Future.delayed(const Duration(milliseconds: 600), () {
      if (!mounted) return;
      if (_emailController.text == 'admin@smartpeel.ai' && _passwordController.text == 'Admin@SmartPeel2026!') {
        ref.read(authProvider.notifier).login(
          'admin@smartpeel.ai',
          'System Administrator',
          true,
        );
        setState(() => _isLoading = false);
        context.go('/admin-dashboard');
      } else {
        setState(() {
          _isLoading = false;
          _errorMessage = 'Invalid administrative credentials.';
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    return Scaffold(
      backgroundColor: const Color(0xFF263238), // Dark slate admin aesthetic
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text(isTamil ? 'நிர்வாக உள்நுழைவு' : 'Admin Security Console'),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 420),
            child: Card(
              color: Colors.white,
              child: Padding(
                padding: const EdgeInsets.all(28.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const Icon(Icons.security_rounded, size: 56, color: Colors.orange),
                    const SizedBox(height: 12),
                    Text(
                      isTamil ? 'நிர்வாக அணுகல்' : 'Administrator Portal',
                      style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.black87),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 6),
                    Text(
                      isTamil ? 'அறிவியல் தரவு மற்றும் ஏஐ மாதிரி மேலாண்மை' : 'Manage scientific sources, models & rules',
                      style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 24),
                    if (_errorMessage != null)
                      Container(
                        padding: const EdgeInsets.all(10),
                        margin: const EdgeInsets.only(bottom: 16),
                        decoration: BoxDecoration(color: Colors.red.shade50, borderRadius: BorderRadius.circular(8)),
                        child: Text(_errorMessage!, style: const TextStyle(color: Colors.red, fontSize: 13)),
                      ),
                    TextField(
                      controller: _emailController,
                      decoration: const InputDecoration(
                        labelText: 'Admin Username / Email',
                        prefixIcon: Icon(Icons.admin_panel_settings_outlined),
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _passwordController,
                      obscureText: true,
                      decoration: const InputDecoration(
                        labelText: 'Secret Passphrase',
                        prefixIcon: Icon(Icons.key_rounded),
                      ),
                    ),
                    const SizedBox(height: 24),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.orange.shade800,
                      ),
                      onPressed: _isLoading ? null : _handleAdminLogin,
                      child: _isLoading
                          ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                          : Text(isTamil ? 'நிர்வாகியாக உள்நுழை' : 'Authorize & Enter Console'),
                    ),
                    const SizedBox(height: 12),
                    TextButton(
                      onPressed: () => context.go('/home'),
                      child: Text(isTamil ? 'பயனர் பகுதிக்கு திரும்பு' : 'Return to User Dashboard'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
