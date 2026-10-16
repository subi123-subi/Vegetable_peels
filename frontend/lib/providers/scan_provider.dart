import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/network/api_client.dart';
import '../models/scan_prediction_model.dart';
import 'app_providers.dart';

class ScanNotifier extends Notifier<AsyncValue<ScanPredictResponseModel?>> {
  final ScanPredictResponseModel? _initialValue;
  ScanNotifier([this._initialValue]);

  @override
  AsyncValue<ScanPredictResponseModel?> build() => AsyncData(_initialValue);

  Future<ScanPredictResponseModel?> predictFromBytes(
    Uint8List bytes,
    String filename, {
    String? previewPath,
  }) async {
    state = const AsyncLoading();
    try {
      final formData = FormData.fromMap({
        'file': MultipartFile.fromBytes(
          bytes,
          filename: filename,
        ),
      });

      final response = await ApiClient().dio.post(
        '/scans/predict',
        data: formData,
        options: Options(
          headers: {'Content-Type': 'multipart/form-data'},
        ),
      );

      final result = ScanPredictResponseModel.fromJson(
        response.data as Map<String, dynamic>,
        localPath: previewPath,
        localBytes: bytes,
      );

      state = AsyncData(result);

      // Sync with global vegetable selected provider if a supported vegetable was predicted
      if (result.isSupportedPeel && result.predictedVegetableSlug != null) {
        final allVegs = ref.read(catalogueProvider);
        try {
          final matchedVeg = allVegs.firstWhere(
            (v) => v.slug == result.predictedVegetableSlug,
          );
          ref.read(selectedVegetableProvider.notifier).select(matchedVeg);
        } catch (_) {}
      }

      return result;
    } catch (e, st) {
      debugPrint('[ScanNotifier] Prediction error: $e');
      state = AsyncError(e, st);
      return null;
    }
  }

  Future<bool> confirmPrediction({
    required int scanId,
    required int confirmedVegetableId,
    int? confirmedPlantPartId,
    double? weightGrams,
    bool isCorrection = false,
    String? notes,
  }) async {
    try {
      final payload = {
        'scan_id': scanId,
        'confirmed_vegetable_id': confirmedVegetableId,
        'confirmed_plant_part_id': confirmedPlantPartId,
        'confirmed_weight_grams': weightGrams,
        'is_correction': isCorrection,
        'user_feedback_notes': notes,
      };

      await ApiClient().dio.post('/scans/confirm', data: payload);
      return true;
    } catch (e) {
      debugPrint('[ScanNotifier] Confirmation error: $e');
      return false;
    }
  }

  void reset() {
    state = const AsyncData(null);
  }

  void setPredictionForTest(ScanPredictResponseModel model) {
    state = AsyncData(model);
  }
}

final scanPredictionProvider =
    NotifierProvider<ScanNotifier, AsyncValue<ScanPredictResponseModel?>>(
  () => ScanNotifier(),
);

final activeModelProvider = FutureProvider<Map<String, dynamic>>((ref) async {
  final response = await ApiClient().dio.get('/scans/models/active');
  return response.data as Map<String, dynamic>;
});
