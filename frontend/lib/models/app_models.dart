class VegetableItem {
  final int id;
  final String slug;
  final String nameEn;
  final String nameTa;
  final String scientificName;
  final String category;
  final String plantPart;
  final bool isAiSupported;
  final String? aiClassName;
  final String nutrientDataStatus; // available, incomplete, unavailable
  final String foodSafetyStatus; // safe_edible, conditional_cooking_required, hazardous_raw, inedible_valorize_only
  final String? knownHazardsEn;
  final String? knownHazardsTa;

  const VegetableItem({
    required this.id,
    required this.slug,
    required this.nameEn,
    required this.nameTa,
    required this.scientificName,
    required this.category,
    required this.plantPart,
    required this.isAiSupported,
    this.aiClassName,
    required this.nutrientDataStatus,
    required this.foodSafetyStatus,
    this.knownHazardsEn,
    this.knownHazardsTa,
  });

  String displayName(bool isTamil) => isTamil ? nameTa : nameEn;

  factory VegetableItem.fromJson(Map<String, dynamic> json) {
    return VegetableItem(
      id: json['id'] as int? ?? 0,
      slug: json['slug'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      nameTa: json['name_ta'] as String? ?? '',
      scientificName: json['scientific_name'] as String? ?? '',
      category: json['category'] as String? ?? '',
      plantPart: json['plant_part'] != null ? json['plant_part']['name_en'] as String? ?? 'peel' : 'peel',
      isAiSupported: json['is_ai_supported'] as bool? ?? false,
      aiClassName: json['ai_class_name'] as String?,
      nutrientDataStatus: json['nutrient_data_status'] as String? ?? 'incomplete',
      foodSafetyStatus: json['food_safety_status'] as String? ?? 'conditional_cooking_required',
      knownHazardsEn: json['known_hazards_en'] as String?,
      knownHazardsTa: json['known_hazards_ta'] as String?,
    );
  }
}

class NutrientItem {
  final String code;
  final String nameEn;
  final String nameTa;
  final String category; // vitamin, mineral, other
  final String unit;
  final double concentrationPer100g;
  final String? biologicalRoleEn;
  final String? biologicalRoleTa;

  const NutrientItem({
    required this.code,
    required this.nameEn,
    required this.nameTa,
    required this.category,
    required this.unit,
    required this.concentrationPer100g,
    this.biologicalRoleEn,
    this.biologicalRoleTa,
  });

  String displayName(bool isTamil) => isTamil ? nameTa : nameEn;
  String displayRole(bool isTamil) => (isTamil ? biologicalRoleTa : biologicalRoleEn) ?? '';

  double calculateAmount(double weightGrams) {
    return (weightGrams / 100.0) * concentrationPer100g;
  }
}

class SafetyRuleItem {
  final String code;
  final String hazardType;
  final String severity; // critical, warning, notice
  final String descriptionEn;
  final String descriptionTa;
  final String? alternativeEn;
  final String? alternativeTa;

  const SafetyRuleItem({
    required this.code,
    required this.hazardType,
    required this.severity,
    required this.descriptionEn,
    required this.descriptionTa,
    this.alternativeEn,
    this.alternativeTa,
  });

  String displayDescription(bool isTamil) => isTamil ? descriptionTa : descriptionEn;
  String displayAlternative(bool isTamil) => (isTamil ? alternativeTa : alternativeEn) ?? '';
}

class ReuseMethodItem {
  final String code;
  final String nameEn;
  final String nameTa;
  final String category;
  final int evidenceRank;
  final String instructionsEn;
  final String instructionsTa;
  final String? warningsEn;
  final String? warningsTa;

  const ReuseMethodItem({
    required this.code,
    required this.nameEn,
    required this.nameTa,
    required this.category,
    required this.evidenceRank,
    required this.instructionsEn,
    required this.instructionsTa,
    this.warningsEn,
    this.warningsTa,
  });

  String displayName(bool isTamil) => isTamil ? nameTa : nameEn;
  String displayInstructions(bool isTamil) => isTamil ? instructionsTa : instructionsEn;
}

class ScanResult {
  final String scanId;
  final String imagePath;
  final VegetableItem predictedVegetable;
  final double confidence;
  final bool isConfirmed;
  final double? weightGrams;
  final DateTime scannedAt;

  const ScanResult({
    required this.scanId,
    required this.imagePath,
    required this.predictedVegetable,
    required this.confidence,
    this.isConfirmed = false,
    this.weightGrams,
    required this.scannedAt,
  });

  ScanResult copyWith({
    bool? isConfirmed,
    VegetableItem? confirmedVegetable,
    double? weightGrams,
  }) {
    return ScanResult(
      scanId: scanId,
      imagePath: imagePath,
      predictedVegetable: confirmedVegetable ?? predictedVegetable,
      confidence: confidence,
      isConfirmed: isConfirmed ?? this.isConfirmed,
      weightGrams: weightGrams ?? this.weightGrams,
      scannedAt: scannedAt,
    );
  }
}
