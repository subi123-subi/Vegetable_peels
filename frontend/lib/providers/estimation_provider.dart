import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/network/api_client.dart';
import '../models/estimation_models.dart';
import 'app_providers.dart';

class EstimationInputParams {
  final double weightGrams;
  final String inputWeightType; // 'peel' or 'whole_vegetable'
  final String preparationMethod; // 'fresh_raw', 'sauteed', 'boiled_broth', 'boiled_drained', 'dried_powder'
  final String populationGroup; // 'adult_male', 'adult_female', 'pregnant_woman', 'lactating_mother', 'children_7_9y'
  final int servings;

  const EstimationInputParams({
    this.weightGrams = 100.0,
    this.inputWeightType = 'peel',
    this.preparationMethod = 'fresh_raw',
    this.populationGroup = 'adult_male',
    this.servings = 1,
  });

  EstimationInputParams copyWith({
    double? weightGrams,
    String? inputWeightType,
    String? preparationMethod,
    String? populationGroup,
    int? servings,
  }) {
    return EstimationInputParams(
      weightGrams: weightGrams ?? this.weightGrams,
      inputWeightType: inputWeightType ?? this.inputWeightType,
      preparationMethod: preparationMethod ?? this.preparationMethod,
      populationGroup: populationGroup ?? this.populationGroup,
      servings: servings ?? this.servings,
    );
  }
}

class EstimationInputNotifier extends Notifier<EstimationInputParams> {
  @override
  EstimationInputParams build() => const EstimationInputParams();

  void setWeight(double weight) {
    if (weight > 0 && weight <= 10000) {
      state = state.copyWith(weightGrams: weight);
    }
  }

  void setInputWeightType(String type) {
    state = state.copyWith(inputWeightType: type);
  }

  void setPreparationMethod(String method) {
    state = state.copyWith(preparationMethod: method);
  }

  void setPopulationGroup(String group) {
    state = state.copyWith(populationGroup: group);
  }

  void setServings(int servings) {
    if (servings >= 1 && servings <= 50) {
      state = state.copyWith(servings: servings);
    }
  }
}

final estimationInputProvider =
    NotifierProvider<EstimationInputNotifier, EstimationInputParams>(
  EstimationInputNotifier.new,
);

class EstimationRepository {
  final Dio _dio;

  EstimationRepository(this._dio);

  Future<List<PeelYieldRatioModel>> fetchAllYieldRatios() async {
    try {
      final response = await _dio.get('/nutrients/yield-ratios');
      if (response.statusCode == 200 && response.data != null) {
        final List<dynamic> list = response.data as List<dynamic>;
        return list.map((json) => PeelYieldRatioModel.fromJson(json as Map<String, dynamic>)).toList();
      }
      return [];
    } catch (e) {
      debugPrint('Error fetching all yield ratios: $e');
      return [];
    }
  }

  Future<PeelYieldRatioModel?> fetchYieldRatio(String slug) async {
    try {
      final response = await _dio.get('/nutrients/yield-ratios/$slug');
      if (response.statusCode == 200 && response.data != null) {
        return PeelYieldRatioModel.fromJson(response.data as Map<String, dynamic>);
      }
      return null;
    } catch (e) {
      debugPrint('Error fetching yield ratio for $slug: $e');
      return null;
    }
  }

  Future<List<DailyReferenceIntakeModel>> fetchDailyReferenceIntakes({String? group}) async {
    try {
      final url = group != null && group.isNotEmpty
          ? '/nutrients/dri?population_group=$group'
          : '/nutrients/dri';
      final response = await _dio.get(url);
      if (response.statusCode == 200 && response.data != null) {
        final List<dynamic> list = response.data as List<dynamic>;
        return list.map((json) => DailyReferenceIntakeModel.fromJson(json as Map<String, dynamic>)).toList();
      }
      return [];
    } catch (e) {
      debugPrint('Error fetching DRIs: $e');
      return [];
    }
  }

  Future<EstimationResultModel?> estimateNutrients({
    required String slug,
    required double weightGrams,
    String inputWeightType = 'peel',
    String preparationMethod = 'fresh_raw',
    String populationGroup = 'adult_male',
    int servings = 1,
  }) async {
    try {
      final payload = {
        'vegetable_slug': slug,
        'input_weight_grams': weightGrams,
        'input_weight_type': inputWeightType,
        'preparation_method': preparationMethod,
        'population_group': populationGroup,
        'servings': servings,
      };
      final response = await _dio.post('/nutrients/estimate', data: payload);
      if (response.statusCode == 200 && response.data != null) {
        return EstimationResultModel.fromJson(response.data as Map<String, dynamic>);
      }
      return null;
    } catch (e) {
      debugPrint('Error calculating nutrient estimation: $e');
      return null;
    }
  }

  Future<NutrientReportModel?> saveReport({
    required int vegetableId,
    required double totalWeightGrams,
    required Map<String, dynamic> calculations,
    Map<String, dynamic>? safetyNotes,
    String? userFeedbackNotes,
  }) async {
    try {
      final payload = {
        'vegetable_id': vegetableId,
        'total_weight_grams': totalWeightGrams,
        'calculations': calculations,
        'safety_notes': safetyNotes,
        'user_feedback_notes': userFeedbackNotes,
      };
      final response = await _dio.post('/nutrients/reports/save', data: payload);
      if (response.statusCode == 201 && response.data != null) {
        return NutrientReportModel.fromJson(response.data as Map<String, dynamic>);
      }
      return null;
    } catch (e) {
      debugPrint('Error saving nutrient report: $e');
      return null;
    }
  }

  Future<NutrientReportModel?> fetchReport(String reportUuid) async {
    try {
      final response = await _dio.get('/nutrients/reports/$reportUuid');
      if (response.statusCode == 200 && response.data != null) {
        return NutrientReportModel.fromJson(response.data as Map<String, dynamic>);
      }
      return null;
    } catch (e) {
      debugPrint('Error fetching nutrient report: $e');
      return null;
    }
  }
}

final estimationRepositoryProvider = Provider<EstimationRepository>((ref) {
  final client = ApiClient();
  return EstimationRepository(client.dio);
});

final allPeelYieldRatiosProvider = FutureProvider<List<PeelYieldRatioModel>>((ref) async {
  final repo = ref.watch(estimationRepositoryProvider);
  return repo.fetchAllYieldRatios();
});

final peelYieldRatioProvider = FutureProvider.family<PeelYieldRatioModel?, String>((ref, slug) async {
  final repo = ref.watch(estimationRepositoryProvider);
  return repo.fetchYieldRatio(slug);
});

final dailyReferenceIntakesProvider =
    FutureProvider.family<List<DailyReferenceIntakeModel>, String>((ref, group) async {
  final repo = ref.watch(estimationRepositoryProvider);
  return repo.fetchDailyReferenceIntakes(group: group);
});

final nutrientEstimationResultProvider = FutureProvider<EstimationResultModel?>((ref) async {
  final veg = ref.watch(selectedVegetableProvider);
  final params = ref.watch(estimationInputProvider);
  final repo = ref.watch(estimationRepositoryProvider);

  if (veg.slug.isEmpty) return null;

  return repo.estimateNutrients(
    slug: veg.slug,
    weightGrams: params.weightGrams,
    inputWeightType: params.inputWeightType,
    preparationMethod: params.preparationMethod,
    populationGroup: params.populationGroup,
    servings: params.servings,
  );
});
