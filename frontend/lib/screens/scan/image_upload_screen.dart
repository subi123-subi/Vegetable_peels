import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../models/app_models.dart';
import '../../providers/app_providers.dart';
import '../../providers/scan_provider.dart';

class ImageUploadScreen extends ConsumerStatefulWidget {
  const ImageUploadScreen({super.key});

  @override
  ConsumerState<ImageUploadScreen> createState() => _ImageUploadScreenState();
}

class _ImageUploadScreenState extends ConsumerState<ImageUploadScreen> {
  final ImagePicker _picker = ImagePicker();
  XFile? _selectedFile;
  Uint8List? _selectedBytes;
  bool _isAnalyzing = false;

  Future<void> _pickImage() async {
    try {
      final XFile? file = await _picker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 1024,
        maxHeight: 1024,
        imageQuality: 85,
      );
      if (file != null) {
        final bytes = await file.readAsBytes();
        setState(() {
          _selectedFile = file;
          _selectedBytes = bytes;
        });
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('File selection error: $e')),
      );
    }
  }

  Future<void> _runIdentification() async {
    if (_selectedBytes == null && _selectedFile == null) return;
    setState(() => _isAnalyzing = true);

    final bytes = _selectedBytes ?? await _selectedFile!.readAsBytes();
    final filename = _selectedFile?.name ?? 'upload.jpg';

    final result = await ref.read(scanPredictionProvider.notifier).predictFromBytes(
      bytes,
      filename,
      previewPath: _selectedFile?.path,
    );

    if (!mounted) return;
    setState(() => _isAnalyzing = false);

    if (result != null) {
      final allVegs = ref.read(catalogueProvider);
      VegetableItem? targetVeg;
      if (result.predictedVegetableSlug != null) {
        targetVeg = allVegs.where((v) => v.slug == result.predictedVegetableSlug).firstOrNull;
      }
      final safeTargetVeg = targetVeg ?? allVegs.first;

      final scanResult = ScanResult(
        scanId: 'SCN-${result.scanId}',
        imagePath: _selectedFile?.path ?? filename,
        predictedVegetable: safeTargetVeg,
        confidence: result.confidence,
        isConfirmed: false,
        scannedAt: result.scannedAt,
      );
      ref.read(currentScanProvider.notifier).setScan(scanResult);
      ref.read(selectedVegetableProvider.notifier).select(safeTargetVeg);

      context.go('/identification');
    } else {
      final err = ref.read(scanPredictionProvider).error;
      final msg = err != null
          ? 'Error: $err'
          : 'AI identification service error. Please try another image.';
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(msg),
          backgroundColor: Colors.red,
          duration: const Duration(seconds: 5),
        ),
      );
    }
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
                        isTamil ? 'JPEG அல்லது PNG வடிவம், 10MB வரை அனுமதிக்கப்படுகிறது' : 'Supports JPG, PNG up to 10MB. Clear natural lighting recommended.',
                        style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 24),

                      // Selected image status or drop-area placeholder
                      if (_selectedBytes != null)
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            border: Border.all(color: AppTheme.primaryGreen, width: 2),
                            borderRadius: BorderRadius.circular(12),
                            color: AppTheme.softMint,
                          ),
                          child: Column(
                            children: [
                              ClipRRect(
                                borderRadius: BorderRadius.circular(8),
                                child: Image.memory(
                                  _selectedBytes!,
                                  height: 180,
                                  fit: BoxFit.cover,
                                ),
                              ),
                              const SizedBox(height: 10),
                              Text(
                                _selectedFile?.name ?? 'Selected Image',
                                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                              ),
                              Text(
                                '${(_selectedBytes!.lengthInBytes / 1024).toStringAsFixed(1)} KB',
                                style: TextStyle(color: Colors.grey.shade600, fontSize: 11),
                              ),
                            ],
                          ),
                        )
                      else
                        InkWell(
                          onTap: _pickImage,
                          borderRadius: BorderRadius.circular(12),
                          child: Container(
                            height: 160,
                            decoration: BoxDecoration(
                              border: Border.all(color: Colors.grey.shade300, width: 2, style: BorderStyle.solid),
                              borderRadius: BorderRadius.circular(12),
                              color: Colors.grey.shade50,
                            ),
                            child: Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.add_photo_alternate_outlined, size: 48, color: Colors.grey.shade400),
                                  const SizedBox(height: 8),
                                  Text(
                                    isTamil ? 'கோப்பை தேர்வு செய்ய கிளிக் செய்க' : 'Click to select an image from device',
                                    style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ),

                      const SizedBox(height: 20),

                      if (_isAnalyzing)
                        const Column(
                          children: [
                            CircularProgressIndicator(color: AppTheme.primaryGreen),
                            SizedBox(height: 12),
                            Text(
                              'Analyzing peel with MobileNetV3 AI Engine...',
                              style: TextStyle(fontWeight: FontWeight.w600, color: AppTheme.primaryDark),
                            ),
                          ],
                        )
                      else
                        Row(
                          children: [
                            Expanded(
                              child: OutlinedButton.icon(
                                onPressed: _pickImage,
                                icon: const Icon(Icons.file_open),
                                label: Text(isTamil ? 'மாற்று படம்' : 'Select File'),
                              ),
                            ),
                            if (_selectedBytes != null) ...[
                              const SizedBox(width: 12),
                              Expanded(
                                child: ElevatedButton.icon(
                                  onPressed: _runIdentification,
                                  icon: const Icon(Icons.analytics_outlined),
                                  label: Text(isTamil ? 'ஆரம்பிக்கவும்' : 'Analyze Peel'),
                                ),
                              ),
                            ],
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
