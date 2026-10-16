import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:smart_peel_ai/models/scan_prediction_model.dart';
import 'package:smart_peel_ai/models/app_models.dart';
import 'package:smart_peel_ai/providers/app_providers.dart';
import 'package:smart_peel_ai/providers/scan_provider.dart';
import 'package:smart_peel_ai/screens/scan/vegetable_identification_screen.dart';

void main() {
  group('Phase 9 AI Scan Models & Provider Tests', () {
    test('ScanPredictResponseModel correctly decodes backend JSON', () {
      final json = {
        'scan_id': 42,
        'prediction_id': 101,
        'predicted_vegetable_slug': 'carrot',
        'predicted_display_name_en': 'Carrot Peel',
        'predicted_display_name_ta': 'கேரட் தோல்',
        'predicted_plant_part': 'Peel / தோல்',
        'confidence': 0.985,
        'model_version': '1.0.0',
        'is_supported_peel': true,
        'confirmation_required': true,
        'is_uncertain': false,
        'top_predictions': [
          {
            'class_key': 'carrot_peel',
            'slug': 'carrot',
            'confidence': 0.985,
            'display_name_en': 'Carrot Peel',
            'display_name_ta': 'கேரட் தோல்',
            'scientific_name': 'Daucus carota subsp. sativus',
            'is_supported_peel': true,
          },
          {
            'class_key': 'pumpkin_peel',
            'slug': 'pumpkin',
            'confidence': 0.012,
            'display_name_en': 'Pumpkin Peel',
            'display_name_ta': 'பூசணிக்காய் தோல்',
            'scientific_name': 'Cucurbita moschata',
            'is_supported_peel': true,
          }
        ],
        'safety_notice': 'Visual identification is probabilistic.',
        'scanned_at': '2026-10-16T16:00:00Z',
      };

      final model = ScanPredictResponseModel.fromJson(json);

      expect(model.scanId, 42);
      expect(model.predictionId, 101);
      expect(model.predictedVegetableSlug, 'carrot');
      expect(model.confidence, 0.985);
      expect(model.isSupportedPeel, isTrue);
      expect(model.isUncertain, isFalse);
      expect(model.topPredictions.length, 2);
      expect(model.topPredictions[0].displayName(true), 'கேரட் தோல்');
      expect(model.topPredictions[0].displayName(false), 'Carrot Peel');
    });

    test('ScanPredictResponseModel correctly handles unsupported negative object', () {
      final json = {
        'scan_id': 43,
        'prediction_id': 102,
        'predicted_vegetable_slug': null,
        'predicted_display_name_en': 'Unsupported / Non-peel Object',
        'predicted_display_name_ta': 'ஆதரிக்கப்படாத பொருள்',
        'predicted_plant_part': 'Peel / தோல்',
        'confidence': 0.991,
        'model_version': '1.0.0',
        'is_supported_peel': false,
        'confirmation_required': true,
        'is_uncertain': true,
        'top_predictions': [],
        'safety_notice': 'Reject non-peel image.',
        'scanned_at': '2026-10-16T16:00:00Z',
      };

      final model = ScanPredictResponseModel.fromJson(json);

      expect(model.isSupportedPeel, isFalse);
      expect(model.isUncertain, isTrue);
      expect(model.predictedVegetableSlug, isNull);
    });

    testWidgets('VegetableIdentificationScreen renders AI prediction and confirmation buttons',
        (tester) async {
      final mockModel = ScanPredictResponseModel(
        scanId: 1,
        predictionId: 10,
        predictedVegetableSlug: 'carrot',
        predictedDisplayNameEn: 'Carrot Peel',
        predictedDisplayNameTa: 'கேரட் தோல்',
        predictedPlantPart: 'Peel / தோல்',
        confidence: 0.965,
        modelVersion: '1.0.0',
        isSupportedPeel: true,
        confirmationRequired: true,
        isUncertain: false,
        topPredictions: [
          const PredictionItemModel(
            classKey: 'carrot_peel',
            slug: 'carrot',
            confidence: 0.965,
            displayNameEn: 'Carrot Peel',
            displayNameTa: 'கேரட் தோல்',
            scientificName: 'Daucus carota subsp. sativus',
            isSupportedPeel: true,
          ),
        ],
        safetyNotice: 'Probabilistic check.',
        scannedAt: DateTime.now(),
      );

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            scanPredictionProvider.overrideWith(() {
              final notifier = ScanNotifier();
              return notifier;
            }),
          ],
          child: const MaterialApp(
            home: Scaffold(
              body: VegetableIdentificationScreen(),
            ),
          ),
        ),
      );

      await tester.pumpAndSettle();

      expect(find.text('MobileNetV3 (v1.0.0)'), findsOneWidget);
      expect(find.byType(DropdownButtonFormField<VegetableItem>), findsOneWidget);
      expect(find.byIcon(Icons.check), findsOneWidget);
      expect(find.byIcon(Icons.replay), findsOneWidget);
    });
  });
}
