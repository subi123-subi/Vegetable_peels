import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:smart_peel_ai/models/estimation_models.dart';
import 'package:smart_peel_ai/providers/estimation_provider.dart';
import 'package:smart_peel_ai/screens/nutrients/nutrient_estimation_screen.dart';

void main() {
  group('Phase 6 Estimation Models Tests', () {
    test('PeelYieldRatioModel deserializes correctly', () {
      final json = {
        'id': 1,
        'vegetable_id': 2,
        'vegetable_slug': 'potato',
        'vegetable_name_en': 'Potato',
        'vegetable_name_ta': 'உருளைக்கிழங்கு',
        'average_peel_percentage': 11.5,
        'min_peel_percentage': 8.0,
        'max_peel_percentage': 15.0,
        'moisture_percentage_fresh': 81.0,
        'dry_matter_percentage': 19.0,
        'water_loss_dehydration_factor': 0.18,
        'pulp_comparison_notes_en': 'High chlorogenic acid in peel periderm.',
        'pulp_comparison_notes_ta': 'தோலில் அதிக குளோரோஜெனிக் அமிலம் உள்ளது.',
        'source_title': 'ICMR-NIN IFCT 2017',
      };

      final model = PeelYieldRatioModel.fromJson(json);
      expect(model.vegetableSlug, 'potato');
      expect(model.averagePeelPercentage, 11.5);
      expect(model.displayName(false), 'Potato');
      expect(model.displayName(true), 'உருளைக்கிழங்கு');
      expect(model.pulpNotes(false), 'High chlorogenic acid in peel periderm.');
      expect(model.pulpNotes(true), 'தோலில் அதிக குளோரோஜெனிக் அமிலம் உள்ளது.');
    });

    test('DailyReferenceIntakeModel deserializes correctly', () {
      final json = {
        'id': 10,
        'nutrient_code': 'vit_c',
        'population_group': 'adult_male',
        'rda_value': 80.0,
        'unit': 'mg',
        'standard_authority': 'ICMR-NIN 2020',
        'notes_en': 'Adult male ascorbic acid requirement',
      };

      final model = DailyReferenceIntakeModel.fromJson(json);
      expect(model.nutrientCode, 'vit_c');
      expect(model.populationGroup, 'adult_male');
      expect(model.rdaValue, 80.0);
      expect(model.unit, 'mg');
    });

    test('EstimationResultModel & Nutrients breakdown deserialize correctly', () {
      final json = {
        'vegetable_id': 1,
        'vegetable_slug': 'carrot',
        'vegetable_name_en': 'Carrot',
        'vegetable_name_ta': 'கேரட்',
        'input_weight_grams': 100.0,
        'input_weight_type': 'peel',
        'calculated_peel_weight_grams': 100.0,
        'peel_weight_range_grams': {'min': 95.0, 'max': 105.0},
        'peel_yield_percentage': 12.0,
        'dry_matter_weight_grams': 11.8,
        'moisture_weight_grams': 88.2,
        'preparation_method': 'sauteed',
        'preparation_method_label_en': 'Sautéed / Stir-Fried',
        'preparation_method_label_ta': 'வறுவல் / பொரியல்',
        'population_group': 'adult_male',
        'population_group_label_en': 'Adult Male',
        'population_group_label_ta': 'வயது வந்த ஆண்',
        'servings': 1,
        'nutrients': [
          {
            'nutrient_code': 'vit_c',
            'nutrient_name_en': 'Vitamin C',
            'nutrient_name_ta': 'வைட்டமின் சி',
            'category': 'vitamin',
            'concentration_per_100g_raw': 16.5,
            'unit': 'mg',
            'retention_factor': 0.80,
            'estimated_amount': 13.2,
            'estimated_amount_per_serving': 13.2,
            'rda_value': 80.0,
            'percentage_rda': 16.5,
            'rda_status': 'good',
            'rda_status_label_en': 'Good Source (15-30% RDA)',
            'rda_status_label_ta': 'நல்ல ஆதாரம் (15-30% RDA)',
          }
        ],
        'environmental_impact': {
          'wet_waste_diverted_kg': 0.1,
          'ghg_emissions_avoided_kg_co2e': 0.052,
          'compost_potential_kg': 0.025,
          'valorization_readiness': 'High',
        },
        'superiority': {
          'comparison_en': 'Carrot peel contains 2.5x higher beta-carotene than core flesh.',
          'comparison_ta': 'கேரட் தோலில் 2.5 மடங்கு அதிக பீட்டா கரோட்டின் உள்ளது.',
          'superior_nutrients': ['Vitamin A', 'Dietary Fibre'],
        },
        'scientific_basis_notes': 'ICMR-NIN IFCT 2017 standards.',
        'timestamp': '2026-10-16T12:00:00Z',
      };

      final result = EstimationResultModel.fromJson(json);
      expect(result.vegetableSlug, 'carrot');
      expect(result.calculatedPeelWeightGrams, 100.0);
      expect(result.nutrients.length, 1);
      expect(result.nutrients.first.nutrientCode, 'vit_c');
      expect(result.nutrients.first.estimatedAmount, 13.2);
      expect(result.nutrients.first.percentageRda, 16.5);
      expect(result.environmentalImpact.wetWasteDivertedKg, 0.1);
      expect(result.environmentalImpact.ghgEmissionsAvoidedKgCo2e, 0.052);
      expect(result.superiority.superiorNutrients.contains('Vitamin A'), true);
    });
  });

  group('Phase 6 Estimation State & UI Widget Tests', () {
    test('EstimationInputNotifier state transitions', () {
      final container = ProviderContainer();
      expect(container.read(estimationInputProvider).weightGrams, 100.0);
      expect(container.read(estimationInputProvider).inputWeightType, 'peel');
      expect(container.read(estimationInputProvider).preparationMethod, 'fresh_raw');

      container.read(estimationInputProvider.notifier).setWeight(250.0);
      expect(container.read(estimationInputProvider).weightGrams, 250.0);

      container.read(estimationInputProvider.notifier).setInputWeightType('whole_vegetable');
      expect(container.read(estimationInputProvider).inputWeightType, 'whole_vegetable');

      container.read(estimationInputProvider.notifier).setPreparationMethod('sauteed');
      expect(container.read(estimationInputProvider).preparationMethod, 'sauteed');

      container.read(estimationInputProvider.notifier).setPopulationGroup('pregnant_woman');
      expect(container.read(estimationInputProvider).populationGroup, 'pregnant_woman');

      container.read(estimationInputProvider.notifier).setServings(4);
      expect(container.read(estimationInputProvider).servings, 4);
    });

    testWidgets('NutrientEstimationScreen renders with weight controls and buttons', (tester) async {
      tester.view.physicalSize = const Size(1200, 900);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(() => tester.view.resetPhysicalSize());

      const mockRatio = PeelYieldRatioModel(
        id: 1,
        vegetableId: 1,
        vegetableSlug: 'carrot',
        vegetableNameEn: 'Carrot',
        vegetableNameTa: 'கேரட்',
        averagePeelPercentage: 12.0,
        minPeelPercentage: 8.5,
        maxPeelPercentage: 16.0,
        moisturePercentageFresh: 88.2,
        dryMatterPercentage: 11.8,
        waterLossDehydrationFactor: 0.14,
        pulpComparisonNotesEn: 'High beta-carotene',
        pulpComparisonNotesTa: 'அதிக பீட்டா கரோட்டின்',
      );

      final mockResult = EstimationResultModel(
        vegetableId: 1,
        vegetableSlug: 'carrot',
        vegetableNameEn: 'Carrot',
        vegetableNameTa: 'கேரட்',
        inputWeightGrams: 100.0,
        inputWeightType: 'peel',
        calculatedPeelWeightGrams: 100.0,
        peelWeightRangeGrams: const {'min': 95.0, 'max': 105.0},
        peelYieldPercentage: 12.0,
        dryMatterWeightGrams: 11.8,
        moistureWeightGrams: 88.2,
        preparationMethod: 'fresh_raw',
        preparationMethodLabelEn: 'Fresh / Raw',
        preparationMethodLabelTa: 'புதிய / பச்சையான',
        populationGroup: 'adult_male',
        populationGroupLabelEn: 'Adult Male',
        populationGroupLabelTa: 'வயது வந்த ஆண்',
        servings: 1,
        nutrients: const [
          NutrientIntakeDetailModel(
            nutrientCode: 'vit_c',
            nutrientNameEn: 'Vitamin C',
            nutrientNameTa: 'வைட்டமின் சி',
            category: 'vitamin',
            concentrationPer100gRaw: 16.5,
            unit: 'mg',
            retentionFactor: 1.0,
            estimatedAmount: 16.5,
            estimatedAmountPerServing: 16.5,
            rdaValue: 80.0,
            percentageRda: 20.6,
            rdaStatus: 'good',
            rdaStatusLabelEn: 'Good Source (15-30% RDA)',
            rdaStatusLabelTa: 'நல்ல ஆதாரம் (15-30% RDA)',
          ),
        ],
        environmentalImpact: const EnvironmentalImpactModel(
          wetWasteDivertedKg: 0.1,
          ghgEmissionsAvoidedKgCo2e: 0.052,
          compostPotentialKg: 0.025,
          valorizationReadiness: 'High',
        ),
        superiority: const NutritionalSuperiorityModel(
          comparisonEn: 'Carrot peel contains 2.5x higher beta-carotene than core flesh.',
          comparisonTa: 'கேரட் தோலில் 2.5 மடங்கு அதிக பீட்டா கரோட்டின் உள்ளது.',
          superiorNutrients: ['Vitamin A'],
        ),
        scientificBasisNotes: 'ICMR-NIN IFCT 2017 standards.',
        timestamp: DateTime.now(),
      );

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            peelYieldRatioProvider.overrideWith((ref, slug) => mockRatio),
            nutrientEstimationResultProvider.overrideWith((ref) => mockResult),
          ],
          child: const MaterialApp(
            home: NutrientEstimationScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Verify app bar title
      expect(find.text('Nutritional Quantity Estimation'), findsOneWidget);

      // Verify weight & measurement basis section
      expect(find.text('Weight & Measurement Basis'), findsOneWidget);
      expect(find.text('Peel Weight'), findsOneWidget);
      expect(find.text('Whole Vegetable'), findsOneWidget);

      // Verify quick portion chips
      expect(find.text('50 g'), findsOneWidget);
      expect(find.text('100 g'), findsOneWidget);
      expect(find.text('250 g'), findsOneWidget);
      expect(find.text('500 g'), findsOneWidget);

      // Verify culinary method section
      expect(find.text('Culinary Method & Target Demographic'), findsOneWidget);
      expect(find.text('🥗 Raw / Fresh'), findsOneWidget);
      expect(find.text('🍳 Sautéed (Poriyal)'), findsOneWidget);

      // Verify calculated result
      expect(find.text('Estimated Nutrient Intake'), findsOneWidget);
      expect(find.text('Vitamin C'), findsOneWidget);
      expect(find.text('16.5 mg'), findsOneWidget);
      expect(find.text('20.6% RDA'), findsOneWidget);
    });
  });
}
