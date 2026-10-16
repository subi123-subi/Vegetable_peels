import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_riverpod/legacy.dart';
import '../core/network/api_client.dart';
import '../models/app_models.dart';
import '../models/vegetable_detail_model.dart';
import 'app_providers.dart';

// Repository Interface & Implementation
class VegetablesRepository {
  final Dio _dio;

  VegetablesRepository(this._dio);

  Future<List<VegetableItem>> fetchAllVegetables() async {
    try {
      final response = await _dio.get('/vegetables/?all=true');
      if (response.statusCode == 200 && response.data != null) {
        final List<dynamic> items = response.data['items'] ?? [];
        return items.map((json) => VegetableItem.fromJson(json as Map<String, dynamic>)).toList();
      }
    } catch (e) {
      debugPrint('[VegetablesRepository] API fetch failed: $e, falling back to local catalogue.');
    }
    // Offline / safe fallback
    return initialCatalogue;
  }

  Future<VegetableFullDetail?> fetchVegetableDetail(String idOrSlug) async {
    try {
      final response = await _dio.get('/vegetables/$idOrSlug');
      if (response.statusCode == 200 && response.data != null) {
        return VegetableFullDetail.fromJson(response.data as Map<String, dynamic>);
      }
    } catch (e) {
      debugPrint('[VegetablesRepository] Failed to fetch vegetable detail: $e');
    }
    return null;
  }

  Future<List<CategoryCountItem>> fetchCategories() async {
    try {
      final response = await _dio.get('/vegetables/categories');
      if (response.statusCode == 200 && response.data != null) {
        final List<dynamic> list = response.data as List<dynamic>;
        return list.map((json) => CategoryCountItem.fromJson(json as Map<String, dynamic>)).toList();
      }
    } catch (e) {
      debugPrint('[VegetablesRepository] Failed to fetch categories: $e');
    }
    return [
      const CategoryCountItem(category: 'Root Vegetable', count: 12),
      const CategoryCountItem(category: 'Gourds & Cucurbits', count: 11),
      const CategoryCountItem(category: 'Solanaceous & Common Roots', count: 8),
      const CategoryCountItem(category: 'Bulbs & Aromatics', count: 5),
      const CategoryCountItem(category: 'Plant Outer Layer', count: 6),
      const CategoryCountItem(category: 'Legumes & Pods', count: 8),
    ];
  }

  Future<List<PlantPartItem>> fetchPlantParts() async {
    try {
      final response = await _dio.get('/vegetables/plant-parts');
      if (response.statusCode == 200 && response.data != null) {
        final List<dynamic> list = response.data as List<dynamic>;
        return list.map((json) => PlantPartItem.fromJson(json as Map<String, dynamic>)).toList();
      }
    } catch (e) {
      debugPrint('[VegetablesRepository] Failed to fetch plant parts: $e');
    }
    return [
      const PlantPartItem(id: 1, code: 'peel', nameEn: 'Vegetable Peel', nameTa: 'காய்கறி தோல்'),
      const PlantPartItem(id: 2, code: 'skin', nameEn: 'Thin Skin', nameTa: 'மெல்லிய தோல்'),
      const PlantPartItem(id: 3, code: 'rind', nameEn: 'Thick Rind', nameTa: 'தடித்த ஓடு'),
      const PlantPartItem(id: 4, code: 'outer_leaves', nameEn: 'Outer Leaves', nameTa: 'வெளிப்புற இலைகள்'),
      const PlantPartItem(id: 5, code: 'pod_shell', nameEn: 'Pod Shell', nameTa: 'நெற்று உறை'),
      const PlantPartItem(id: 6, code: 'stem_layer', nameEn: 'Stem Outer Layer', nameTa: 'தண்டு வெளிப்புற அடுக்கு'),
      const PlantPartItem(id: 7, code: 'husk', nameEn: 'Husk / Sheath', nameTa: 'உமி / உறை'),
    ];
  }

  Future<bool> createVegetable(Map<String, dynamic> payload) async {
    try {
      final response = await _dio.post('/vegetables/', data: payload);
      return response.statusCode == 201;
    } catch (e) {
      debugPrint('[VegetablesRepository] Create failed: $e');
      rethrow;
    }
  }

  Future<bool> updateVegetable(int id, Map<String, dynamic> payload) async {
    try {
      final response = await _dio.put('/vegetables/$id', data: payload);
      return response.statusCode == 200;
    } catch (e) {
      debugPrint('[VegetablesRepository] Update failed: $e');
      rethrow;
    }
  }

  Future<bool> deleteVegetable(int id, {bool permanent = false}) async {
    try {
      final response = await _dio.delete('/vegetables/$id?permanent=$permanent');
      return response.statusCode == 200;
    } catch (e) {
      debugPrint('[VegetablesRepository] Delete failed: $e');
      rethrow;
    }
  }
}

// Providers
final vegetablesRepositoryProvider = Provider<VegetablesRepository>((ref) {
  final client = ApiClient();
  return VegetablesRepository(client.dio);
});

// Async Vegetables List
final vegetablesListAsyncProvider = FutureProvider<List<VegetableItem>>((ref) async {
  final repo = ref.watch(vegetablesRepositoryProvider);
  return repo.fetchAllVegetables();
});

// Categories with Counts
final categoriesAsyncProvider = FutureProvider<List<CategoryCountItem>>((ref) async {
  final repo = ref.watch(vegetablesRepositoryProvider);
  return repo.fetchCategories();
});

// Plant Parts List
final plantPartsAsyncProvider = FutureProvider<List<PlantPartItem>>((ref) async {
  final repo = ref.watch(vegetablesRepositoryProvider);
  return repo.fetchPlantParts();
});

// Filter States
final selectedCategoryFilterProvider = StateProvider<String>((ref) => 'All');
final searchQueryFilterProvider = StateProvider<String>((ref) => '');
final aiSupportedFilterProvider = StateProvider<bool?>((ref) => null);
final safetyStatusFilterProvider = StateProvider<String?>((ref) => null);

// Filtered List Computed Provider
final filteredVegetablesListProvider = Provider<List<VegetableItem>>((ref) {
  final asyncVegs = ref.watch(vegetablesListAsyncProvider);
  final vegs = asyncVegs.value ?? initialCatalogue;

  final selectedCategory = ref.watch(selectedCategoryFilterProvider);
  final searchQuery = ref.watch(searchQueryFilterProvider).trim().toLowerCase();
  final aiOnly = ref.watch(aiSupportedFilterProvider);
  final safetyStatus = ref.watch(safetyStatusFilterProvider);

  return vegs.where((v) {
    // 1. AI Supported Filter
    if (aiOnly != null && aiOnly == true && !v.isAiSupported) {
      return false;
    }

    // 2. Category Filter
    if (selectedCategory != 'All') {
      if (selectedCategory == 'AI Ready') {
        if (!v.isAiSupported) return false;
      } else if (!v.category.toLowerCase().contains(selectedCategory.toLowerCase())) {
        return false;
      }
    }

    // 3. Safety Status Filter
    if (safetyStatus != null && safetyStatus.isNotEmpty && safetyStatus != 'All') {
      if (v.foodSafetyStatus != safetyStatus) return false;
    }

    // 4. Search Filter (English, Tamil, Botanical Name, Slug)
    if (searchQuery.isNotEmpty) {
      final matchEn = v.nameEn.toLowerCase().contains(searchQuery);
      final matchTa = v.nameTa.toLowerCase().contains(searchQuery);
      final matchSci = v.scientificName.toLowerCase().contains(searchQuery);
      final matchSlug = v.slug.toLowerCase().contains(searchQuery);
      if (!matchEn && !matchTa && !matchSci && !matchSlug) {
        return false;
      }
    }

    return true;
  }).toList();
});

// Vegetable Detail by Slug or ID Provider
final vegetableDetailAsyncProvider = FutureProvider.family<VegetableFullDetail?, String>((ref, slugOrId) async {
  final repo = ref.watch(vegetablesRepositoryProvider);
  return repo.fetchVegetableDetail(slugOrId);
});
