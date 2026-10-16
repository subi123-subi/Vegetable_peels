import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../models/app_models.dart';
import '../../providers/app_providers.dart';

class ImageUploadScreen extends ConsumerStatefulWidget {
  const ImageUploadScreen({super.key});

  @override
  ConsumerState<ImageUploadScreen> createState() => _ImageUploadScreenState();
}

class _ImageUploadScreenState extends ConsumerState<ImageUploadScreen> {
  final ImagePicker _picker = ImagePicker();
  XFile? _selectedFile;
  bool _isAnalyzing = false;

  Future<void> _pickImage() async {
    try {
      final XFile? file = await _picker.pickImage(source: ImageSource.gallery);
      if (file != null) {
        setState(() {
          _selectedFile = file;
        });
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('File selection error: $e')),
      );
    }
  }

  void _runIdentification(VegetableItem targetVeg) {
    setState(() => _isAnalyzing = true);
    Future.delayed(const Duration(milliseconds: 800), () {
      final scanResult = ScanResult(
        scanId: 'SCN-${DateTime.now().millisecondsSinceEpoch.toString().substring(7)}',
        imagePath: _selectedFile?.path ?? 'sample_upload.jpg',
        predictedVegetable: targetVeg,
        confidence: 0.92,
        isConfirmed: false,
        scannedAt: DateTime.now(),
      );
      ref.read(currentScanProvider.notifier).setScan(scanResult);
      ref.read(selectedVegetableProvider.notifier).select(targetVeg);
      if (!mounted) return;
      setState(() => _isAnalyzing = false);
      context.go('/identification');
    });
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 650),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    children: [
                      const Icon(Icons.cloud_upload_outlined, size: 64, color: AppTheme.primaryGreen),
                      const SizedBox(height: 12),
                      Text(
                        isTamil ? 'புகைப்படத்தை பதிவேற்றவும்' : 'Upload Vegetable Peel Photograph',
                        style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        isTamil ? 'JPEG அல்லது PNG வடிவம், தெளிவான வெளிச்சம்' : 'Supports JPG, PNG up to 10MB. Clear natural lighting recommended.',
                        style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 24),

                      // Selected image status or drop-area placeholder
                      Container(
                        height: 200,
                        width: double.infinity,
                        decoration: BoxDecoration(
                          color: AppTheme.surfaceMuted,
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(color: Colors.grey.shade300, style: BorderStyle.solid),
                        ),
                        child: _selectedFile != null
                            ? Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  const Icon(Icons.check_circle, color: AppTheme.primaryGreen, size: 48),
                                  const SizedBox(height: 12),
                                  Text(
                                    'Selected: ${_selectedFile!.name}',
                                    style: const TextStyle(fontWeight: FontWeight.bold),
                                  ),
                                  const SizedBox(height: 6),
                                  TextButton(
                                    onPressed: _pickImage,
                                    child: const Text('Change File'),
                                  ),
                                ],
                              )
                            : Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  const Icon(Icons.add_photo_alternate_outlined, size: 48, color: Colors.grey),
                                  const SizedBox(height: 8),
                                  Text(
                                    isTamil ? 'கோப்பை தேர்வு செய்ய கிளிக் செய்யவும்' : 'Click to Browse Files',
                                    style: TextStyle(color: Colors.grey.shade700, fontWeight: FontWeight.w600),
                                  ),
                                ],
                              ),
                      ),
                      const SizedBox(height: 20),

                      ElevatedButton.icon(
                        onPressed: _isAnalyzing ? null : _pickImage,
                        icon: const Icon(Icons.folder_open),
                        label: Text(isTamil ? 'கோப்பகத்திலிருந்து தேர்வு செய்க' : 'Browse Gallery / Files'),
                        style: ElevatedButton.styleFrom(
                          minimumSize: const Size(double.infinity, 50),
                        ),
                      ),

                      if (_selectedFile != null) ...[
                        const SizedBox(height: 12),
                        ElevatedButton.icon(
                          onPressed: _isAnalyzing ? null : () => _runIdentification(initialCatalogue[0]),
                          icon: const Icon(Icons.analytics_outlined),
                          label: _isAnalyzing
                              ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                              : Text(isTamil ? 'ஏஐ மூலம் ஆய்வு செய்க' : 'Run AI Identification'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppTheme.leafGreen,
                            minimumSize: const Size(double.infinity, 50),
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // Preset Samples Shortcut
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        isTamil ? 'விரைவு சோதனை மாதிரிகள்:' : 'Or Select a Preset Test Sample:',
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                      ),
                      const SizedBox(height: 10),
                      Wrap(
                        spacing: 8,
                        children: [
                          ChoiceChip(
                            label: const Text('Carrot Peel'),
                            selected: false,
                            onSelected: (_) => _runIdentification(initialCatalogue[0]),
                          ),
                          ChoiceChip(
                            label: const Text('Potato Peel'),
                            selected: false,
                            onSelected: (_) => _runIdentification(initialCatalogue[1]),
                          ),
                          ChoiceChip(
                            label: const Text('Beetroot Peel'),
                            selected: false,
                            onSelected: (_) => _runIdentification(initialCatalogue[2]),
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
