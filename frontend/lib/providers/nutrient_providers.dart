import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/network/api_client.dart';
import '../models/vegetable_detail_model.dart';

class ScientificSourceItem {
  final int id;
  final String title;
  final String? authors;
  final int? publicationYear;
  final String? journalOrPublisher;
  final String? doiOrUrl;
  final String sourceType;
  final String reliabilityRating;

  const ScientificSourceItem({
    required this.id,
    required this.title,
    this.authors,
    this.publicationYear,
    this.journalOrPublisher,
    this.doiOrUrl,
    required this.sourceType,
    required this.reliabilityRating,
  });

  factory ScientificSourceItem.fromJson(Map<String, dynamic> json) {
    return ScientificSourceItem(
      id: json['id'] as int? ?? 0,
      title: json['title'] as String? ?? '',
      authors: json['authors'] as String?,
      publicationYear: json['publication_year'] as int?,
      journalOrPublisher: json['journal_or_publisher'] as String?,
      doiOrUrl: json['doi_or_url'] as String?,
      sourceType: json['source_type'] as String? ?? 'peer_reviewed',
      reliabilityRating: json['reliability_rating'] as String? ?? 'high',
    );
  }
}

class NutrientMasterItem {
  final int id;
  final String code;
  final String nameEn;
  final String nameTa;
  final String category; // vitamin, mineral, other
  final String standardUnit;
  final String? descriptionEn;
  final String? descriptionTa;
  final String? biologicalRoleEn;
  final String? biologicalRoleTa;

  const NutrientMasterItem({
    required this.id,
    required this.code,
    required this.nameEn,
    required this.nameTa,
    required this.category,
    required this.standardUnit,
    this.descriptionEn,
    this.descriptionTa,
    this.biologicalRoleEn,
    this.biologicalRoleTa,
  });

  String displayName(bool isTamil) => isTamil ? nameTa : nameEn;
  String displayRole(bool isTamil) => (isTamil ? biologicalRoleTa : biologicalRoleEn) ?? '';

  factory NutrientMasterItem.fromJson(Map<String, dynamic> json) {
    return NutrientMasterItem(
      id: json['id'] as int? ?? 0,
      code: json['code'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      nameTa: json['name_ta'] as String? ?? '',
      category: json['category'] as String? ?? 'other',
      standardUnit: json['standard_unit'] as String? ?? 'mg',
      descriptionEn: json['description_en'] as String?,
      descriptionTa: json['description_ta'] as String?,
      biologicalRoleEn: json['biological_role_en'] as String?,
      biologicalRoleTa: json['biological_role_ta'] as String?,
    );
  }
}

class TopSourceItem {
  final int vegetableId;
  final String vegetableSlug;
  final String vegetableNameEn;
  final String vegetableNameTa;
  final double concentrationPer100g;
  final String unit;
  final String dataQualityStatus;

  const TopSourceItem({
    required this.vegetableId,
    required this.vegetableSlug,
    required this.vegetableNameEn,
    required this.vegetableNameTa,
    required this.concentrationPer100g,
    required this.unit,
    required this.dataQualityStatus,
  });

  String displayName(bool isTamil) => isTamil ? vegetableNameTa : vegetableNameEn;

  factory TopSourceItem.fromJson(Map<String, dynamic> json) {
    return TopSourceItem(
      vegetableId: json['vegetable_id'] as int? ?? 0,
      vegetableSlug: json['vegetable_slug'] as String? ?? '',
      vegetableNameEn: json['vegetable_name_en'] as String? ?? '',
      vegetableNameTa: json['vegetable_name_ta'] as String? ?? '',
      concentrationPer100g: (json['concentration_per_100g'] as num?)?.toDouble() ?? 0.0,
      unit: json['unit'] as String? ?? 'mg',
      dataQualityStatus: json['data_quality_status'] as String? ?? 'validated_peel_measurement',
    );
  }
}

class NutrientDetailWithSources {
  final NutrientMasterItem nutrient;
  final List<TopSourceItem> topPeelSources;

  const NutrientDetailWithSources({
    required this.nutrient,
    required this.topPeelSources,
  });

  factory NutrientDetailWithSources.fromJson(Map<String, dynamic> json) {
    final sourcesList = (json['top_peel_sources'] as List<dynamic>?) ?? [];
    return NutrientDetailWithSources(
      nutrient: NutrientMasterItem.fromJson(json),
      topPeelSources: sourcesList.map((s) => TopSourceItem.fromJson(s as Map<String, dynamic>)).toList(),
    );
  }
}

class FullNutrientProfile {
  final int id;
  final int vegetableId;
  final String vegetableSlug;
  final String vegetableNameEn;
  final String vegetableNameTa;
  final String plantPartCode;
  final String freshOrDryBasis;
  final String? samplePrepMethod;
  final String? uncertaintyNotes;
  final String dataQualityStatus;
  final ScientificSourceItem? source;
  final List<NutrientDetailItem> measurements;

  const FullNutrientProfile({
    required this.id,
    required this.vegetableId,
    required this.vegetableSlug,
    required this.vegetableNameEn,
    required this.vegetableNameTa,
    required this.plantPartCode,
    required this.freshOrDryBasis,
    this.samplePrepMethod,
    this.uncertaintyNotes,
    required this.dataQualityStatus,
    this.source,
    required this.measurements,
  });

  factory FullNutrientProfile.fromJson(Map<String, dynamic> json) {
    final measList = (json['measurements'] as List<dynamic>?) ?? [];
    return FullNutrientProfile(
      id: json['id'] as int? ?? 0,
      vegetableId: json['vegetable_id'] as int? ?? 0,
      vegetableSlug: json['vegetable_slug'] as String? ?? '',
      vegetableNameEn: json['vegetable_name_en'] as String? ?? '',
      vegetableNameTa: json['vegetable_name_ta'] as String? ?? '',
      plantPartCode: json['plant_part_code'] as String? ?? 'peel',
      freshOrDryBasis: json['fresh_or_dry_basis'] as String? ?? 'fresh_weight',
      samplePrepMethod: json['sample_prep_method'] as String?,
      uncertaintyNotes: json['uncertainty_notes'] as String?,
      dataQualityStatus: json['data_quality_status'] as String? ?? 'validated_peel_measurement',
      source: json['source'] != null ? ScientificSourceItem.fromJson(json['source'] as Map<String, dynamic>) : null,
      measurements: measList.map((m) => NutrientDetailItem.fromJson(m as Map<String, dynamic>)).toList(),
    );
  }
}

class NutrientsRepository {
  final Dio _dio;

  NutrientsRepository(this._dio);

  Future<List<NutrientMasterItem>> fetchNutrients({String? category}) async {
    try {
      final url = category != null && category.isNotEmpty && category != 'all'
          ? '/nutrients/?category=$category'
          : '/nutrients/';
      final response = await _dio.get(url);
      if (response.statusCode == 200 && response.data != null) {
        final List<dynamic> list = response.data as List<dynamic>;
        return list.map((json) => NutrientMasterItem.fromJson(json as Map<String, dynamic>)).toList();
      }
    } catch (e) {
      debugPrint('[NutrientsRepository] Fetch nutrients failed: $e');
    }
    return [];
  }

  Future<List<ScientificSourceItem>> fetchSources() async {
    try {
      final response = await _dio.get('/nutrients/sources');
      if (response.statusCode == 200 && response.data != null) {
        final List<dynamic> list = response.data as List<dynamic>;
        return list.map((json) => ScientificSourceItem.fromJson(json as Map<String, dynamic>)).toList();
      }
    } catch (e) {
      debugPrint('[NutrientsRepository] Fetch sources failed: $e');
    }
    return [];
  }

  Future<FullNutrientProfile?> fetchVegetableProfile(String slug) async {
    try {
      final response = await _dio.get('/nutrients/profiles/$slug');
      if (response.statusCode == 200 && response.data != null) {
        return FullNutrientProfile.fromJson(response.data as Map<String, dynamic>);
      }
    } catch (e) {
      debugPrint('[NutrientsRepository] Fetch profile for $slug failed: $e');
    }
    return null;
  }

  Future<NutrientDetailWithSources?> fetchNutrientWithTopSources(String code) async {
    try {
      final response = await _dio.get('/nutrients/$code');
      if (response.statusCode == 200 && response.data != null) {
        return NutrientDetailWithSources.fromJson(response.data as Map<String, dynamic>);
      }
    } catch (e) {
      debugPrint('[NutrientsRepository] Fetch nutrient detail for $code failed: $e');
    }
    return null;
  }

  Future<bool> createNutrient(Map<String, dynamic> payload) async {
    try {
      final response = await _dio.post('/nutrients/', data: payload);
      return response.statusCode == 201;
    } catch (e) {
      debugPrint('[NutrientsRepository] Create nutrient failed: $e');
      rethrow;
    }
  }

  Future<bool> addMeasurement(Map<String, dynamic> payload) async {
    try {
      final response = await _dio.post('/nutrients/measurements', data: payload);
      return response.statusCode == 201;
    } catch (e) {
      debugPrint('[NutrientsRepository] Add measurement failed: $e');
      rethrow;
    }
  }
}

// Providers
final nutrientsRepositoryProvider = Provider<NutrientsRepository>((ref) {
  final client = ApiClient();
  return NutrientsRepository(client.dio);
});

final allNutrientsAsyncProvider = FutureProvider<List<NutrientMasterItem>>((ref) async {
  final repo = ref.watch(nutrientsRepositoryProvider);
  return repo.fetchNutrients();
});

final vitaminsAsyncProvider = FutureProvider<List<NutrientMasterItem>>((ref) async {
  final repo = ref.watch(nutrientsRepositoryProvider);
  return repo.fetchNutrients(category: 'vitamin');
});

final mineralsAsyncProvider = FutureProvider<List<NutrientMasterItem>>((ref) async {
  final repo = ref.watch(nutrientsRepositoryProvider);
  return repo.fetchNutrients(category: 'mineral');
});

final bioactivesAsyncProvider = FutureProvider<List<NutrientMasterItem>>((ref) async {
  final repo = ref.watch(nutrientsRepositoryProvider);
  return repo.fetchNutrients(category: 'other');
});

final scientificSourcesAsyncProvider = FutureProvider<List<ScientificSourceItem>>((ref) async {
  final repo = ref.watch(nutrientsRepositoryProvider);
  return repo.fetchSources();
});

final vegetableNutrientProfileAsyncProvider = FutureProvider.family<FullNutrientProfile?, String>((ref, slug) async {
  final repo = ref.watch(nutrientsRepositoryProvider);
  return repo.fetchVegetableProfile(slug);
});

final nutrientWithTopSourcesAsyncProvider = FutureProvider.family<NutrientDetailWithSources?, String>((ref, code) async {
  final repo = ref.watch(nutrientsRepositoryProvider);
  return repo.fetchNutrientWithTopSources(code);
});
