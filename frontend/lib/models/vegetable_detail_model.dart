class PlantPartItem {
  final int id;
  final String code;
  final String nameEn;
  final String nameTa;
  final String? descriptionEn;
  final String? descriptionTa;

  const PlantPartItem({
    required this.id,
    required this.code,
    required this.nameEn,
    required this.nameTa,
    this.descriptionEn,
    this.descriptionTa,
  });

  String displayName(bool isTamil) => isTamil ? nameTa : nameEn;

  factory PlantPartItem.fromJson(Map<String, dynamic> json) {
    return PlantPartItem(
      id: json['id'] as int? ?? 0,
      code: json['code'] as String? ?? 'peel',
      nameEn: json['name_en'] as String? ?? 'Peel',
      nameTa: json['name_ta'] as String? ?? 'தோல்',
      descriptionEn: json['description_en'] as String?,
      descriptionTa: json['description_ta'] as String?,
    );
  }
}

class CategoryCountItem {
  final String category;
  final int count;

  const CategoryCountItem({required this.category, required this.count});

  factory CategoryCountItem.fromJson(Map<String, dynamic> json) {
    return CategoryCountItem(
      category: json['category'] as String? ?? '',
      count: json['count'] as int? ?? 0,
    );
  }
}

class NutrientDetailItem {
  final int nutrientId;
  final String nutrientCode;
  final String nutrientNameEn;
  final String nutrientNameTa;
  final String category; // vitamin, mineral, other
  final double concentrationPer100g;
  final String unit;
  final String? biologicalRoleEn;
  final String? biologicalRoleTa;
  final String? dataQualityStatus;

  const NutrientDetailItem({
    required this.nutrientId,
    required this.nutrientCode,
    required this.nutrientNameEn,
    required this.nutrientNameTa,
    required this.category,
    required this.concentrationPer100g,
    required this.unit,
    this.biologicalRoleEn,
    this.biologicalRoleTa,
    this.dataQualityStatus,
  });

  String displayName(bool isTamil) => isTamil ? nutrientNameTa : nutrientNameEn;
  String displayRole(bool isTamil) => (isTamil ? biologicalRoleTa : biologicalRoleEn) ?? '';

  factory NutrientDetailItem.fromJson(Map<String, dynamic> json) {
    return NutrientDetailItem(
      nutrientId: json['nutrient_id'] as int? ?? 0,
      nutrientCode: json['nutrient_code'] as String? ?? '',
      nutrientNameEn: json['nutrient_name_en'] as String? ?? '',
      nutrientNameTa: json['nutrient_name_ta'] as String? ?? '',
      category: json['category'] as String? ?? 'other',
      concentrationPer100g: (json['concentration_per_100g'] as num?)?.toDouble() ?? 0.0,
      unit: json['unit'] as String? ?? 'mg',
      biologicalRoleEn: json['biological_role_en'] as String?,
      biologicalRoleTa: json['biological_role_ta'] as String?,
      dataQualityStatus: json['data_quality_status'] as String?,
    );
  }
}

class SafetyRuleDetailItem {
  final int id;
  final String code;
  final String hazardType;
  final String severity; // critical, warning, notice
  final String ruleDescriptionEn;
  final String ruleDescriptionTa;
  final String? alternativeEn;
  final String? alternativeTa;

  const SafetyRuleDetailItem({
    required this.id,
    required this.code,
    required this.hazardType,
    required this.severity,
    required this.ruleDescriptionEn,
    required this.ruleDescriptionTa,
    this.alternativeEn,
    this.alternativeTa,
  });

  String displayDescription(bool isTamil) => isTamil ? ruleDescriptionTa : ruleDescriptionEn;
  String displayAlternative(bool isTamil) => (isTamil ? alternativeTa : alternativeEn) ?? '';

  factory SafetyRuleDetailItem.fromJson(Map<String, dynamic> json) {
    return SafetyRuleDetailItem(
      id: json['id'] as int? ?? 0,
      code: json['code'] as String? ?? '',
      hazardType: json['hazard_type'] as String? ?? '',
      severity: json['severity'] as String? ?? 'warning',
      ruleDescriptionEn: json['rule_description_en'] as String? ?? '',
      ruleDescriptionTa: json['rule_description_ta'] as String? ?? '',
      alternativeEn: json['conservative_alternative_en'] as String?,
      alternativeTa: json['conservative_alternative_ta'] as String?,
    );
  }
}

class ReuseRecommendationDetailItem {
  final int id;
  final String methodCode;
  final String methodNameEn;
  final String methodNameTa;
  final String category;
  final int evidenceRank;
  final String instructionsEn;
  final String instructionsTa;
  final String? warningsEn;
  final String? warningsTa;

  const ReuseRecommendationDetailItem({
    required this.id,
    required this.methodCode,
    required this.methodNameEn,
    required this.methodNameTa,
    required this.category,
    required this.evidenceRank,
    required this.instructionsEn,
    required this.instructionsTa,
    this.warningsEn,
    this.warningsTa,
  });

  String displayName(bool isTamil) => isTamil ? methodNameTa : methodNameEn;
  String displayInstructions(bool isTamil) => isTamil ? instructionsTa : instructionsEn;

  factory ReuseRecommendationDetailItem.fromJson(Map<String, dynamic> json) {
    return ReuseRecommendationDetailItem(
      id: json['id'] as int? ?? 0,
      methodCode: json['method_code'] as String? ?? '',
      methodNameEn: json['method_name_en'] as String? ?? '',
      methodNameTa: json['method_name_ta'] as String? ?? '',
      category: json['category'] as String? ?? 'General',
      evidenceRank: json['evidence_rank'] as int? ?? 1,
      instructionsEn: json['preparation_instructions_en'] as String? ?? '',
      instructionsTa: json['preparation_instructions_ta'] as String? ?? '',
      warningsEn: json['limitations_and_warnings_en'] as String?,
      warningsTa: json['limitations_and_warnings_ta'] as String?,
    );
  }
}

class VegetableFullDetail {
  final int id;
  final String slug;
  final String nameEn;
  final String nameTa;
  final String scientificName;
  final String category;
  final int plantPartId;
  final PlantPartItem? plantPart;
  final String? descriptionEn;
  final String? descriptionTa;
  final bool isAiSupported;
  final String? aiClassName;
  final String nutrientDataStatus;
  final String foodSafetyStatus;
  final String? knownHazardsEn;
  final String? knownHazardsTa;
  final List<SafetyRuleDetailItem> safetyRules;
  final List<NutrientDetailItem> nutrients;
  final List<ReuseRecommendationDetailItem> reuseRecommendations;

  const VegetableFullDetail({
    required this.id,
    required this.slug,
    required this.nameEn,
    required this.nameTa,
    required this.scientificName,
    required this.category,
    required this.plantPartId,
    this.plantPart,
    this.descriptionEn,
    this.descriptionTa,
    required this.isAiSupported,
    this.aiClassName,
    required this.nutrientDataStatus,
    required this.foodSafetyStatus,
    this.knownHazardsEn,
    this.knownHazardsTa,
    required this.safetyRules,
    required this.nutrients,
    required this.reuseRecommendations,
  });

  String displayName(bool isTamil) => isTamil ? nameTa : nameEn;
  String displayDescription(bool isTamil) => (isTamil ? descriptionTa : descriptionEn) ?? '';

  factory VegetableFullDetail.fromJson(Map<String, dynamic> json) {
    final rulesList = (json['safety_rules'] as List<dynamic>?) ?? [];
    final nutrientsList = (json['nutrients'] as List<dynamic>?) ?? [];
    final reusesList = (json['reuse_recommendations'] as List<dynamic>?) ?? [];

    return VegetableFullDetail(
      id: json['id'] as int? ?? 0,
      slug: json['slug'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      nameTa: json['name_ta'] as String? ?? '',
      scientificName: json['scientific_name'] as String? ?? '',
      category: json['category'] as String? ?? '',
      plantPartId: json['plant_part_id'] as int? ?? 1,
      plantPart: json['plant_part'] != null ? PlantPartItem.fromJson(json['plant_part'] as Map<String, dynamic>) : null,
      descriptionEn: json['description_en'] as String?,
      descriptionTa: json['description_ta'] as String?,
      isAiSupported: json['is_ai_supported'] as bool? ?? false,
      aiClassName: json['ai_class_name'] as String?,
      nutrientDataStatus: json['nutrient_data_status'] as String? ?? 'incomplete',
      foodSafetyStatus: json['food_safety_status'] as String? ?? 'conditional_cooking_required',
      knownHazardsEn: json['known_hazards_en'] as String?,
      knownHazardsTa: json['known_hazards_ta'] as String?,
      safetyRules: rulesList.map((r) => SafetyRuleDetailItem.fromJson(r as Map<String, dynamic>)).toList(),
      nutrients: nutrientsList.map((n) => NutrientDetailItem.fromJson(n as Map<String, dynamic>)).toList(),
      reuseRecommendations: reusesList.map((rec) => ReuseRecommendationDetailItem.fromJson(rec as Map<String, dynamic>)).toList(),
    );
  }
}
