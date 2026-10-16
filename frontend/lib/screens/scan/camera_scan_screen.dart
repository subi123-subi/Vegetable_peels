import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../models/app_models.dart';
import '../../providers/app_providers.dart';

class CameraScanScreen extends ConsumerStatefulWidget {
  const CameraScanScreen({super.key});

  @override
  ConsumerState<CameraScanScreen> createState() => _CameraScanScreenState();
}

class _CameraScanScreenState extends ConsumerState<CameraScanScreen> {
  final ImagePicker _picker = ImagePicker();
  bool _isProcessing = false;

  Future<void> _captureWithCamera() async {
    setState(() => _isProcessing = true);
    try {
      final XFile? photo = await _picker.pickImage(source: ImageSource.camera);
      if (photo != null) {
        _simulateAIInference(photo.path, initialCatalogue[0]); // Defaults to Carrot for demo
      } else {
        setState(() => _isProcessing = false);
      }
    } catch (e) {
      // Platform doesn't have active camera hardware (e.g. desktop), fallback gracefully
      setState(() => _isProcessing = false);
      _showDesktopCameraNotice();
    }
  }

  void _simulateAIInference(String path, VegetableItem veg) {
    setState(() => _isProcessing = true);
    Future.delayed(const Duration(milliseconds: 900), () {
      final scanResult = ScanResult(
        scanId: 'SCN-${DateTime.now().millisecondsSinceEpoch.toString().substring(7)}',
        imagePath: path,
        predictedVegetable: veg,
        confidence: 0.94,
        isConfirmed: false,
        scannedAt: DateTime.now(),
      );
      ref.read(currentScanProvider.notifier).setScan(scanResult);
      ref.read(selectedVegetableProvider.notifier).select(veg);
      if (!mounted) return;
      setState(() => _isProcessing = false);
      context.go('/identification');
    });
  }

  void _showDesktopCameraNotice() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Camera hardware not detected. You can upload an image or click a quick-test sample below!'),
        backgroundColor: Colors.orange,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20.0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 700),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Instructions Card
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    children: [
                      const Icon(Icons.tips_and_updates_outlined, color: AppTheme.primaryGreen),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          isTamil
                              ? 'தோல் பகுதியை மையமாக வைத்து, நல்ல வெளிச்சத்தில் படம் எடுக்கவும்.'
                              : 'Center peel in the viewfinder. Ensure uniform lighting for optimal AI classification.',
                          style: const TextStyle(fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 16),

              // Viewfinder Viewport
              Container(
                height: 380,
                decoration: BoxDecoration(
                  color: Colors.black87,
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(color: AppTheme.primaryGreen, width: 2),
                ),
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    // Corner guide brackets
                    Positioned(
                      top: 40,
                      left: 40,
                      child: Container(width: 32, height: 32, decoration: const BoxDecoration(border: Border(top: BorderSide(color: Colors.lightGreenAccent, width: 3), left: BorderSide(color: Colors.lightGreenAccent, width: 3)))),
                    ),
                    Positioned(
                      top: 40,
                      right: 40,
                      child: Container(width: 32, height: 32, decoration: const BoxDecoration(border: Border(top: BorderSide(color: Colors.lightGreenAccent, width: 3), right: BorderSide(color: Colors.lightGreenAccent, width: 3)))),
                    ),
                    Positioned(
                      bottom: 40,
                      left: 40,
                      child: Container(width: 32, height: 32, decoration: const BoxDecoration(border: Border(bottom: BorderSide(color: Colors.lightGreenAccent, width: 3), left: BorderSide(color: Colors.lightGreenAccent, width: 3)))),
                    ),
                    Positioned(
                      bottom: 40,
                      right: 40,
                      child: Container(width: 32, height: 32, decoration: const BoxDecoration(border: Border(bottom: BorderSide(color: Colors.lightGreenAccent, width: 3), right: BorderSide(color: Colors.lightGreenAccent, width: 3)))),
                    ),

                    // Central Viewport Target
                    Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.center_focus_strong, size: 72, color: Colors.white54),
                        const SizedBox(height: 12),
                        Text(
                          isTamil ? 'காய்கறி தோலை இங்கே பொருத்தவும்' : 'Align Vegetable Peel Here',
                          style: const TextStyle(color: Colors.white70, fontSize: 14),
                        ),
                      ],
                    ),

                    if (_isProcessing)
                      Container(
                        color: Colors.black54,
                        child: const Center(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              CircularProgressIndicator(color: Colors.lightGreenAccent),
                              SizedBox(height: 16),
                              Text(
                                'MobileNetV3 Analyzing Texture & Features...',
                                style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                              ),
                            ],
                          ),
                        ),
                      ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Capture Action Buttons
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  OutlinedButton.icon(
                    onPressed: () => context.go('/image-upload'),
                    icon: const Icon(Icons.photo_library),
                    label: Text(isTamil ? 'கேலரி' : 'Gallery'),
                  ),
                  const SizedBox(width: 16),
                  ElevatedButton.icon(
                    onPressed: _isProcessing ? null : _captureWithCamera,
                    icon: const Icon(Icons.camera_alt),
                    label: Text(isTamil ? 'படம் எடு' : 'Capture Sample'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 28),

              // Quick Test Simulators for Desktop / Review
              Card(
                color: Colors.white,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        isTamil ? 'பரிசோதனை மாதிரிகள் (டெஸ்க்டாப் / சோதனைக்கு):' : 'Direct Sample Testers (for testing & verification):',
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: AppTheme.primaryDark),
                      ),
                      const SizedBox(height: 12),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          ActionChip(
                            avatar: const Icon(Icons.science, size: 16, color: Colors.orange),
                            label: const Text('Carrot Peel (கேரட்)'),
                            onPressed: () => _simulateAIInference('assets/sample_carrot.jpg', initialCatalogue[0]),
                          ),
                          ActionChip(
                            avatar: const Icon(Icons.science, size: 16, color: Colors.brown),
                            label: const Text('Potato Peel (உருளை)'),
                            onPressed: () => _simulateAIInference('assets/sample_potato.jpg', initialCatalogue[1]),
                          ),
                          ActionChip(
                            avatar: const Icon(Icons.science, size: 16, color: Colors.purple),
                            label: const Text('Beetroot Peel (பீட்ரூட்)'),
                            onPressed: () => _simulateAIInference('assets/sample_beetroot.jpg', initialCatalogue[2]),
                          ),
                          ActionChip(
                            avatar: const Icon(Icons.science, size: 16, color: Colors.green),
                            label: const Text('Cucumber Peel (வெள்ளரி)'),
                            onPressed: () => _simulateAIInference('assets/sample_cucumber.jpg', initialCatalogue[3]),
                          ),
                          ActionChip(
                            avatar: const Icon(Icons.science, size: 16, color: Colors.amber),
                            label: const Text('Pumpkin Peel (பூசணி)'),
                            onPressed: () => _simulateAIInference('assets/sample_pumpkin.jpg', initialCatalogue[4]),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
