import 'dart:typed_data';

class PredictionItemModel {
  final String classKey;
  final String slug;
  final double confidence;
  final String displayNameEn;
  final String displayNameTa;
  final String scientificName;
  final bool isSupportedPeel;

  const PredictionItemModel({
    required this.classKey,
    required this.slug,
    required this.confidence,
    required this.displayNameEn,
    required this.displayNameTa,
    required this.scientificName,
    required this.isSupportedPeel,
  });

  String displayName(bool isTamil) => isTamil ? displayNameTa : displayNameEn;

  factory PredictionItemModel.fromJson(Map<String, dynamic> json) {
    return PredictionItemModel(
      classKey: json['class_key'] as String? ?? '',
      slug: json['slug'] as String? ?? '',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
      displayNameEn: json['display_name_en'] as String? ?? '',
      displayNameTa: json['display_name_ta'] as String? ?? '',
      scientificName: json['scientific_name'] as String? ?? '',
      isSupportedPeel: json['is_supported_peel'] as bool? ?? false,
    );
  }
}

class ScanPredictResponseModel {
  final int scanId;
  final int predictionId;
  final String? predictedVegetableSlug;
  final String predictedDisplayNameEn;
  final String predictedDisplayNameTa;
  final String predictedPlantPart;
  final double confidence;
  final String modelVersion;
  final bool isSupportedPeel;
  final bool confirmationRequired;
  final bool isUncertain;
  final List<PredictionItemModel> topPredictions;
  final String safetyNotice;
  final DateTime scannedAt;
  final String? localImagePreviewPath;
  final Uint8List? localImageBytes;

  const ScanPredictResponseModel({
    required this.scanId,
    required this.predictionId,
    this.predictedVegetableSlug,
    required this.predictedDisplayNameEn,
    required this.predictedDisplayNameTa,
    required this.predictedPlantPart,
    required this.confidence,
    required this.modelVersion,
    required this.isSupportedPeel,
    required this.confirmationRequired,
    required this.isUncertain,
    required this.topPredictions,
    required this.safetyNotice,
    required this.scannedAt,
    this.localImagePreviewPath,
    this.localImageBytes,
  });

  String displayName(bool isTamil) => isTamil ? predictedDisplayNameTa : predictedDisplayNameEn;

  ScanPredictResponseModel copyWithImage({
    String? path,
    Uint8List? bytes,
  }) {
    return ScanPredictResponseModel(
      scanId: scanId,
      predictionId: predictionId,
      predictedVegetableSlug: predictedVegetableSlug,
      predictedDisplayNameEn: predictedDisplayNameEn,
      predictedDisplayNameTa: predictedDisplayNameTa,
      predictedPlantPart: predictedPlantPart,
      confidence: confidence,
      modelVersion: modelVersion,
      isSupportedPeel: isSupportedPeel,
      confirmationRequired: confirmationRequired,
      isUncertain: isUncertain,
      topPredictions: topPredictions,
      safetyNotice: safetyNotice,
      scannedAt: scannedAt,
      localImagePreviewPath: path ?? localImagePreviewPath,
      localImageBytes: bytes ?? localImageBytes,
    );
  }

  factory ScanPredictResponseModel.fromJson(
    Map<String, dynamic> json, {
    String? localPath,
    Uint8List? localBytes,
  }) {
    final rawTop = json['top_predictions'] as List<dynamic>? ?? [];
    return ScanPredictResponseModel(
      scanId: json['scan_id'] as int? ?? 0,
      predictionId: json['prediction_id'] as int? ?? 0,
      predictedVegetableSlug: json['predicted_vegetable_slug'] as String?,
      predictedDisplayNameEn: json['predicted_display_name_en'] as String? ?? 'Unknown',
      predictedDisplayNameTa: json['predicted_display_name_ta'] as String? ?? 'தெரியாத பொருள்',
      predictedPlantPart: json['predicted_plant_part'] as String? ?? 'Peel / தோல்',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
      modelVersion: json['model_version'] as String? ?? '1.0.0',
      isSupportedPeel: json['is_supported_peel'] as bool? ?? false,
      confirmationRequired: json['confirmation_required'] as bool? ?? true,
      isUncertain: json['is_uncertain'] as bool? ?? false,
      topPredictions: rawTop
          .map((item) => PredictionItemModel.fromJson(item as Map<String, dynamic>))
          .toList(),
      safetyNotice: json['safety_notice'] as String? ?? '',
      scannedAt: json['scanned_at'] != null
          ? DateTime.tryParse(json['scanned_at'] as String) ?? DateTime.now()
          : DateTime.now(),
      localImagePreviewPath: localPath,
      localImageBytes: localBytes,
    );
  }
}
