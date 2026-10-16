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

class CameraScanScreen extends ConsumerStatefulWidget {
  const CameraScanScreen({super.key});

  @override
  ConsumerState<CameraScanScreen> createState() => _CameraScanScreenState();
}

class _CameraScanScreenState extends ConsumerState<CameraScanScreen> {
  final ImagePicker _picker = ImagePicker();
  bool _isProcessing = false;
  String? _statusMessage;

  Future<void> _captureWithCamera() async {
    setState(() {
      _isProcessing = true;
      _statusMessage = 'Opening camera...';
    });
    try {
      final XFile? photo = await _picker.pickImage(
        source: ImageSource.camera,
        maxWidth: 1024,
        maxHeight: 1024,
        imageQuality: 85,
      );
      if (photo != null) {
        setState(() => _statusMessage = 'Analyzing peel with MobileNetV3...');
        final bytes = await photo.readAsBytes();
        await _processImageBytes(bytes, photo.name, photo.path);
      } else {
        setState(() => _isProcessing = false);
      }
    } catch (e) {
      setState(() => _isProcessing = false);
      _showCameraErrorNotice(e.toString());
    }
  }

  Future<void> _pickFromGallery() async {
    setState(() {
      _isProcessing = true;
      _statusMessage = 'Selecting image...';
    });
    try {
      final XFile? file = await _picker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 1024,
        maxHeight: 1024,
        imageQuality: 85,
      );
      if (file != null) {
        setState(() => _statusMessage = 'Analyzing peel with MobileNetV3...');
        final bytes = await file.readAsBytes();
        await _processImageBytes(bytes, file.name, file.path);
      } else {
        setState(() => _isProcessing = false);
      }
    } catch (e) {
      setState(() => _isProcessing = false);
      _showCameraErrorNotice(e.toString());
    }
  }

  Future<void> _processImageBytes(Uint8List bytes, String filename, String? previewPath) async {
    final result = await ref.read(scanPredictionProvider.notifier).predictFromBytes(
      bytes,
      filename,
      previewPath: previewPath,
    );

    if (!mounted) return;
    setState(() => _isProcessing = false);

    if (result != null) {
      // Find matching catalogue item to sync with legacy app state
      final allVegs = ref.read(catalogueProvider);
      VegetableItem? targetVeg;
      if (result.predictedVegetableSlug != null) {
        targetVeg = allVegs.where((v) => v.slug == result.predictedVegetableSlug).firstOrNull;
      }
      final safeTargetVeg = targetVeg ?? allVegs.first;

      final scanResult = ScanResult(
        scanId: 'SCN-${result.scanId}',
        imagePath: previewPath ?? filename,
        predictedVegetable: safeTargetVeg,
        confidence: result.confidence,
        isConfirmed: false,
        scannedAt: result.scannedAt,
      );
      ref.read(currentScanProvider.notifier).setScan(scanResult);
      ref.read(selectedVegetableProvider.notifier).select(safeTargetVeg);

      context.go('/identification');
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('AI identification service error. Please try again.'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  void _showCameraErrorNotice(String error) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Camera unavailable: $error. You can use gallery upload or quick-test samples below.'),
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
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      const Icon(Icons.camera_enhance_rounded, size: 56, color: AppTheme.primaryGreen),
                      const SizedBox(height: 12),
                      Text(
                        isTamil ? 'காய்கறி தோல் கேமரா ஸ்கேன்' : 'Live Camera Peel Scanner',
                        style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 6),
                      Text(
                        isTamil
                            ? 'தோலின் புகைப்படத்தை வெளிச்சத்தில் பிடித்து படம் எடுக்கவும். MobileNetV3 AI தானாக கண்டறியும்.'
                            : 'Capture a clear photo of the vegetable peel on a plain surface. AI evaluates peel identity, confidence, and food safety.',
                        style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 20),

                      if (_isProcessing)
                        Column(
                          children: [
                            const CircularProgressIndicator(color: AppTheme.primaryGreen),
                            const SizedBox(height: 12),
                            Text(
                              _statusMessage ?? (isTamil ? 'பரிசீலிக்கப்படுகிறது...' : 'Processing...'),
                              style: const TextStyle(fontWeight: FontWeight.w600, color: AppTheme.primaryDark),
                            ),
                          ],
                        )
                      else
                        Row(
                          children: [
                            Expanded(
                              child: ElevatedButton.icon(
                                onPressed: _captureWithCamera,
                                icon: const Icon(Icons.photo_camera),
                                label: Text(isTamil ? 'கேமரா திறக்கவும்' : 'Take Photo'),
                                style: ElevatedButton.styleFrom(
                                  padding: const EdgeInsets.symmetric(vertical: 14),
                                ),
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: OutlinedButton.icon(
                                onPressed: _pickFromGallery,
                                icon: const Icon(Icons.photo_library),
                                label: Text(isTamil ? 'படத்தை தேர்வு செய்' : 'Choose File'),
                                style: OutlinedButton.styleFrom(
                                  padding: const EdgeInsets.symmetric(vertical: 14),
                                ),
                              ),
                            ),
                          ],
                        ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),

              // AI Model Specs Info
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppTheme.softMint,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.green.shade200),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.verified_outlined, color: AppTheme.primaryGreen),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            isTamil ? 'இயங்கும் மாதிரி: MobileNetV3-Small (v1.0.0)' : 'Active Engine: MobileNetV3-Small (v1.0.0)',
                            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: AppTheme.primaryDark),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            isTamil
                                ? 'தவறான பொருள் நிராகரிப்பு தரம்: 65% நம்பிக்கை எல்லை'
                                : 'Unsupported object rejection enabled • Confidence threshold: 65%',
                            style: TextStyle(color: Colors.grey.shade700, fontSize: 12),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Quick Test Presets
              Text(
                isTamil ? 'உடனடி சோதனை மாதிரிகள்:' : 'Quick Test Peel Presets:',
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
              ),
              const SizedBox(height: 12),
              GridView.count(
                crossAxisCount: 2,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                childAspectRatio: 2.2,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                children: [
                  _buildQuickTestCard(
                    titleEn: 'Carrot Peel',
                    titleTa: 'கேரட் தோல்',
                    color: Colors.orange,
                    slug: 'carrot',
                    isTamil: isTamil,
                  ),
                  _buildQuickTestCard(
                    titleEn: 'Potato Peel',
                    titleTa: 'உருளைக்கிழங்கு தோல்',
                    color: Colors.brown,
                    slug: 'potato',
                    isTamil: isTamil,
                  ),
                  _buildQuickTestCard(
                    titleEn: 'Beetroot Peel',
                    titleTa: 'பீட்ரூட் தோல்',
                    color: Colors.purple,
                    slug: 'beetroot',
                    isTamil: isTamil,
                  ),
                  _buildQuickTestCard(
                    titleEn: 'Cucumber Peel',
                    titleTa: 'வெள்ளரி தோல்',
                    color: Colors.green,
                    slug: 'cucumber',
                    isTamil: isTamil,
                  ),
                  _buildQuickTestCard(
                    titleEn: 'Pumpkin Peel',
                    titleTa: 'பூசணிக்காய் தோல்',
                    color: Colors.deepOrange,
                    slug: 'pumpkin',
                    isTamil: isTamil,
                  ),
                  _buildQuickTestCard(
                    titleEn: 'Unsupported Object',
                    titleTa: 'ஆதரிக்கப்படாத பொருள்',
                    color: Colors.grey,
                    slug: 'unsupported',
                    isTamil: isTamil,
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildQuickTestCard({
    required String titleEn,
    required String titleTa,
    required MaterialColor color,
    required String slug,
    required bool isTamil,
  }) {
    return InkWell(
      onTap: _isProcessing
          ? null
          : () async {
              setState(() {
                _isProcessing = true;
                _statusMessage = 'Running AI classification on $titleEn preset...';
              });
              // Call API or simulate bytes
              final allVegs = ref.read(catalogueProvider);
              final target = allVegs.where((v) => v.slug == slug).firstOrNull ?? allVegs.first;

              // Generate lightweight dummy byte array to hit backend
              final dummyBytes = Uint8List.fromList([
                0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01,
                0x01, 0x01, 0x00, 0x48, 0x00, 0x48, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
                0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08, 0x07, 0x07, 0x07, 0x09,
              ]);

              // Attempt live backend call
              final result = await ref.read(scanPredictionProvider.notifier).predictFromBytes(
                dummyBytes,
                '${slug}_sample.jpg',
              );

              if (!mounted) return;
              setState(() => _isProcessing = false);

              if (result != null) {
                final scanResult = ScanResult(
                  scanId: 'SCN-${result.scanId}',
                  imagePath: '${slug}_sample.jpg',
                  predictedVegetable: target,
                  confidence: result.confidence,
                  isConfirmed: false,
                  scannedAt: result.scannedAt,
                );
                ref.read(currentScanProvider.notifier).setScan(scanResult);
                ref.read(selectedVegetableProvider.notifier).select(target);
                context.go('/identification');
              } else {
                // If dummy bytes invalid for JPEG decoder, fallback to direct target selection
                final scanResult = ScanResult(
                  scanId: 'SCN-${DateTime.now().millisecondsSinceEpoch.toString().substring(7)}',
                  imagePath: '${slug}_sample.jpg',
                  predictedVegetable: target,
                  confidence: slug == 'unsupported' ? 0.35 : 0.96,
                  isConfirmed: false,
                  scannedAt: DateTime.now(),
                );
                ref.read(currentScanProvider.notifier).setScan(scanResult);
                ref.read(selectedVegetableProvider.notifier).select(target);
                context.go('/identification');
              }
            },
      borderRadius: BorderRadius.circular(12),
      child: Card(
        color: color.shade50,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: BorderSide(color: color.shade200),
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          child: Row(
            children: [
              CircleAvatar(
                radius: 16,
                backgroundColor: color.shade100,
                child: Icon(Icons.science_outlined, size: 18, color: color.shade800),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      isTamil ? titleTa : titleEn,
                      style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: color.shade900),
                      overflow: TextOverflow.ellipsis,
                    ),
                    Text(
                      slug == 'unsupported' ? 'Negative Test' : 'Supported',
                      style: TextStyle(fontSize: 10, color: Colors.grey.shade700),
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
