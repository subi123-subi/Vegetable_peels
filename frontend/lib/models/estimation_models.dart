class PeelYieldRatioModel {
  final int id;
  final int vegetableId;
  final String vegetableSlug;
  final String vegetableNameEn;
  final String vegetableNameTa;
  final double averagePeelPercentage;
  final double minPeelPercentage;
  final double maxPeelPercentage;
  final double moisturePercentageFresh;
  final double dryMatterPercentage;
  final double waterLossDehydrationFactor;
  final String? pulpComparisonNotesEn;
  final String? pulpComparisonNotesTa;
  final String? sourceTitle;

  const PeelYieldRatioModel({
    required this.id,
    required this.vegetableId,
    required this.vegetableSlug,
    required this.vegetableNameEn,
    required this.vegetableNameTa,
    required this.averagePeelPercentage,
    required this.minPeelPercentage,
    required this.maxPeelPercentage,
    required this.moisturePercentageFresh,
    required this.dryMatterPercentage,
    required this.waterLossDehydrationFactor,
    this.pulpComparisonNotesEn,
    this.pulpComparisonNotesTa,
    this.sourceTitle,
  });

  String displayName(bool isTamil) => isTamil ? vegetableNameTa : vegetableNameEn;
  String pulpNotes(bool isTamil) => (isTamil ? pulpComparisonNotesTa : pulpComparisonNotesEn) ?? '';

  factory PeelYieldRatioModel.fromJson(Map<String, dynamic> json) {
    return PeelYieldRatioModel(
      id: json['id'] as int? ?? 0,
      vegetableId: json['vegetable_id'] as int? ?? 0,
      vegetableSlug: json['vegetable_slug'] as String? ?? '',
      vegetableNameEn: json['vegetable_name_en'] as String? ?? '',
      vegetableNameTa: json['vegetable_name_ta'] as String? ?? '',
      averagePeelPercentage: (json['average_peel_percentage'] as num?)?.toDouble() ?? 15.0,
      minPeelPercentage: (json['min_peel_percentage'] as num?)?.toDouble() ?? 10.0,
      maxPeelPercentage: (json['max_peel_percentage'] as num?)?.toDouble() ?? 20.0,
      moisturePercentageFresh: (json['moisture_percentage_fresh'] as num?)?.toDouble() ?? 88.0,
      dryMatterPercentage: (json['dry_matter_percentage'] as num?)?.toDouble() ?? 12.0,
      waterLossDehydrationFactor: (json['water_loss_dehydration_factor'] as num?)?.toDouble() ?? 0.15,
      pulpComparisonNotesEn: json['pulp_comparison_notes_en'] as String?,
      pulpComparisonNotesTa: json['pulp_comparison_notes_ta'] as String?,
      sourceTitle: json['source_title'] as String?,
    );
  }
}

class DailyReferenceIntakeModel {
  final int id;
  final String nutrientCode;
  final String populationGroup;
  final double rdaValue;
  final String unit;
  final String standardAuthority;
  final String? notesEn;
  final String? notesTa;

  const DailyReferenceIntakeModel({
    required this.id,
    required this.nutrientCode,
    required this.populationGroup,
    required this.rdaValue,
    required this.unit,
    required this.standardAuthority,
    this.notesEn,
    this.notesTa,
  });

  factory DailyReferenceIntakeModel.fromJson(Map<String, dynamic> json) {
    return DailyReferenceIntakeModel(
      id: json['id'] as int? ?? 0,
      nutrientCode: json['nutrient_code'] as String? ?? '',
      populationGroup: json['population_group'] as String? ?? 'adult_male',
      rdaValue: (json['rda_value'] as num?)?.toDouble() ?? 0.0,
      unit: json['unit'] as String? ?? 'mg',
      standardAuthority: json['standard_authority'] as String? ?? 'ICMR-NIN 2020',
      notesEn: json['notes_en'] as String?,
      notesTa: json['notes_ta'] as String?,
    );
  }
}

class NutrientIntakeDetailModel {
  final String nutrientCode;
  final String nutrientNameEn;
  final String nutrientNameTa;
  final String category; // vitamin, mineral, other
  final double concentrationPer100gRaw;
  final String unit;
  final double retentionFactor;
  final double estimatedAmount;
  final double estimatedAmountPerServing;
  final double? minEstimatedAmount;
  final double? maxEstimatedAmount;
  final String? confidenceInterval;
  final double? rdaValue;
  final double? percentageRda;
  final String? rdaStatus; // exceptional, good, moderate, trace
  final String? rdaStatusLabelEn;
  final String? rdaStatusLabelTa;
  final String? biologicalRoleEn;
  final String? biologicalRoleTa;

  const NutrientIntakeDetailModel({
    required this.nutrientCode,
    required this.nutrientNameEn,
    required this.nutrientNameTa,
    required this.category,
    required this.concentrationPer100gRaw,
    required this.unit,
    required this.retentionFactor,
    required this.estimatedAmount,
    required this.estimatedAmountPerServing,
    this.minEstimatedAmount,
    this.maxEstimatedAmount,
    this.confidenceInterval,
    this.rdaValue,
    this.percentageRda,
    this.rdaStatus,
    this.rdaStatusLabelEn,
    this.rdaStatusLabelTa,
    this.biologicalRoleEn,
    this.biologicalRoleTa,
  });

  String displayName(bool isTamil) => isTamil ? nutrientNameTa : nutrientNameEn;
  String rdaLabel(bool isTamil) => (isTamil ? rdaStatusLabelTa : rdaStatusLabelEn) ?? '';
  String biologicalRole(bool isTamil) => (isTamil ? biologicalRoleTa : biologicalRoleEn) ?? '';

  factory NutrientIntakeDetailModel.fromJson(Map<String, dynamic> json) {
    return NutrientIntakeDetailModel(
      nutrientCode: json['nutrient_code'] as String? ?? '',
      nutrientNameEn: json['nutrient_name_en'] as String? ?? '',
      nutrientNameTa: json['nutrient_name_ta'] as String? ?? '',
      category: json['category'] as String? ?? 'other',
      concentrationPer100gRaw: (json['concentration_per_100g_raw'] as num?)?.toDouble() ?? 0.0,
      unit: json['unit'] as String? ?? 'mg',
      retentionFactor: (json['retention_factor'] as num?)?.toDouble() ?? 1.0,
      estimatedAmount: (json['estimated_amount'] as num?)?.toDouble() ?? 0.0,
      estimatedAmountPerServing: (json['estimated_amount_per_serving'] as num?)?.toDouble() ?? 0.0,
      minEstimatedAmount: (json['min_estimated_amount'] as num?)?.toDouble(),
      maxEstimatedAmount: (json['max_estimated_amount'] as num?)?.toDouble(),
      confidenceInterval: json['confidence_interval'] as String?,
      rdaValue: (json['rda_value'] as num?)?.toDouble(),
      percentageRda: (json['percentage_rda'] as num?)?.toDouble(),
      rdaStatus: json['rda_status'] as String?,
      rdaStatusLabelEn: json['rda_status_label_en'] as String?,
      rdaStatusLabelTa: json['rda_status_label_ta'] as String?,
      biologicalRoleEn: json['biological_role_en'] as String?,
      biologicalRoleTa: json['biological_role_ta'] as String?,
    );
  }
}

class EnvironmentalImpactModel {
  final double wetWasteDivertedKg;
  final double ghgEmissionsAvoidedKgCo2e;
  final double compostPotentialKg;
  final String valorizationReadiness;

  const EnvironmentalImpactModel({
    required this.wetWasteDivertedKg,
    required this.ghgEmissionsAvoidedKgCo2e,
    required this.compostPotentialKg,
    required this.valorizationReadiness,
  });

  factory EnvironmentalImpactModel.fromJson(Map<String, dynamic> json) {
    return EnvironmentalImpactModel(
      wetWasteDivertedKg: (json['wet_waste_diverted_kg'] as num?)?.toDouble() ?? 0.0,
      ghgEmissionsAvoidedKgCo2e: (json['ghg_emissions_avoided_kg_co2e'] as num?)?.toDouble() ?? 0.0,
      compostPotentialKg: (json['compost_potential_kg'] as num?)?.toDouble() ?? 0.0,
      valorizationReadiness: json['valorization_readiness'] as String? ?? '',
    );
  }
}

class NutritionalSuperiorityModel {
  final String comparisonEn;
  final String comparisonTa;
  final List<String> superiorNutrients;

  const NutritionalSuperiorityModel({
    required this.comparisonEn,
    required this.comparisonTa,
    required this.superiorNutrients,
  });

  String comparison(bool isTamil) => isTamil ? comparisonTa : comparisonEn;

  factory NutritionalSuperiorityModel.fromJson(Map<String, dynamic> json) {
    final list = (json['superior_nutrients'] as List<dynamic>?) ?? [];
    return NutritionalSuperiorityModel(
      comparisonEn: json['comparison_en'] as String? ?? '',
      comparisonTa: json['comparison_ta'] as String? ?? '',
      superiorNutrients: list.map((e) => e.toString()).toList(),
    );
  }
}

class EstimationResultModel {
  final int vegetableId;
  final String vegetableSlug;
  final String vegetableNameEn;
  final String vegetableNameTa;
  final double inputWeightGrams;
  final String inputWeightType;
  final double calculatedPeelWeightGrams;
  final Map<String, double> peelWeightRangeGrams;
  final double peelYieldPercentage;
  final double dryMatterWeightGrams;
  final double moistureWeightGrams;
  final String preparationMethod;
  final String preparationMethodLabelEn;
  final String preparationMethodLabelTa;
  final String populationGroup;
  final String populationGroupLabelEn;
  final String populationGroupLabelTa;
  final int servings;
  final List<NutrientIntakeDetailModel> nutrients;
  final EnvironmentalImpactModel environmentalImpact;
  final NutritionalSuperiorityModel superiority;
  final String scientificBasisNotes;
  final DateTime timestamp;

  const EstimationResultModel({
    required this.vegetableId,
    required this.vegetableSlug,
    required this.vegetableNameEn,
    required this.vegetableNameTa,
    required this.inputWeightGrams,
    required this.inputWeightType,
    required this.calculatedPeelWeightGrams,
    required this.peelWeightRangeGrams,
    required this.peelYieldPercentage,
    required this.dryMatterWeightGrams,
    required this.moistureWeightGrams,
    required this.preparationMethod,
    required this.preparationMethodLabelEn,
    required this.preparationMethodLabelTa,
    required this.populationGroup,
    required this.populationGroupLabelEn,
    required this.populationGroupLabelTa,
    required this.servings,
    required this.nutrients,
    required this.environmentalImpact,
    required this.superiority,
    required this.scientificBasisNotes,
    required this.timestamp,
  });

  String displayName(bool isTamil) => isTamil ? vegetableNameTa : vegetableNameEn;
  String prepLabel(bool isTamil) => isTamil ? preparationMethodLabelTa : preparationMethodLabelEn;
  String popGroupLabel(bool isTamil) => isTamil ? populationGroupLabelTa : populationGroupLabelEn;

  factory EstimationResultModel.fromJson(Map<String, dynamic> json) {
    final nuts = (json['nutrients'] as List<dynamic>?) ?? [];
    final rangeMap = (json['peel_weight_range_grams'] as Map<String, dynamic>?) ?? {};
    final env = json['environmental_impact'] as Map<String, dynamic>? ?? {};
    final sup = json['superiority'] as Map<String, dynamic>? ?? {};

    return EstimationResultModel(
      vegetableId: json['vegetable_id'] as int? ?? 0,
      vegetableSlug: json['vegetable_slug'] as String? ?? '',
      vegetableNameEn: json['vegetable_name_en'] as String? ?? '',
      vegetableNameTa: json['vegetable_name_ta'] as String? ?? '',
      inputWeightGrams: (json['input_weight_grams'] as num?)?.toDouble() ?? 100.0,
      inputWeightType: json['input_weight_type'] as String? ?? 'peel',
      calculatedPeelWeightGrams: (json['calculated_peel_weight_grams'] as num?)?.toDouble() ?? 100.0,
      peelWeightRangeGrams: {
        'min': (rangeMap['min'] as num?)?.toDouble() ?? 95.0,
        'max': (rangeMap['max'] as num?)?.toDouble() ?? 105.0,
      },
      peelYieldPercentage: (json['peel_yield_percentage'] as num?)?.toDouble() ?? 15.0,
      dryMatterWeightGrams: (json['dry_matter_weight_grams'] as num?)?.toDouble() ?? 15.0,
      moistureWeightGrams: (json['moisture_weight_grams'] as num?)?.toDouble() ?? 85.0,
      preparationMethod: json['preparation_method'] as String? ?? 'fresh_raw',
      preparationMethodLabelEn: json['preparation_method_label_en'] as String? ?? 'Fresh / Raw',
      preparationMethodLabelTa: json['preparation_method_label_ta'] as String? ?? 'புதிய / பச்சையான',
      populationGroup: json['population_group'] as String? ?? 'adult_male',
      populationGroupLabelEn: json['population_group_label_en'] as String? ?? 'Adult Male',
      populationGroupLabelTa: json['population_group_label_ta'] as String? ?? 'வயது வந்த ஆண்',
      servings: json['servings'] as int? ?? 1,
      nutrients: nuts.map((e) => NutrientIntakeDetailModel.fromJson(e as Map<String, dynamic>)).toList(),
      environmentalImpact: EnvironmentalImpactModel.fromJson(env),
      superiority: NutritionalSuperiorityModel.fromJson(sup),
      scientificBasisNotes: json['scientific_basis_notes'] as String? ?? '',
      timestamp: DateTime.tryParse(json['timestamp'] as String? ?? '') ?? DateTime.now(),
    );
  }
}

class NutrientReportModel {
  final int id;
  final String reportUuid;
  final int? confirmationId;
  final double? totalWeightGrams;
  final Map<String, dynamic> calculations;
  final Map<String, dynamic> safetyNotes;
  final DateTime createdAt;

  const NutrientReportModel({
    required this.id,
    required this.reportUuid,
    this.confirmationId,
    this.totalWeightGrams,
    required this.calculations,
    required this.safetyNotes,
    required this.createdAt,
  });

  factory NutrientReportModel.fromJson(Map<String, dynamic> json) {
    return NutrientReportModel(
      id: json['id'] as int? ?? 0,
      reportUuid: json['report_uuid'] as String? ?? '',
      confirmationId: json['confirmation_id'] as int?,
      totalWeightGrams: (json['total_weight_grams'] as num?)?.toDouble(),
      calculations: (json['calculations'] as Map<String, dynamic>?) ?? {},
      safetyNotes: (json['safety_notes'] as Map<String, dynamic>?) ?? {},
      createdAt: DateTime.tryParse(json['created_at'] as String? ?? '') ?? DateTime.now(),
    );
  }
}
