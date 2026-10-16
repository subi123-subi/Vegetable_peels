import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_peel_ai/screens/nutrients/nutrient_results_screen.dart';
import 'package:smart_peel_ai/screens/nutrients/vitamin_details_screen.dart';
import 'package:smart_peel_ai/screens/nutrients/mineral_details_screen.dart';
import 'package:smart_peel_ai/providers/app_providers.dart';
import 'package:smart_peel_ai/providers/nutrient_providers.dart';

void main() {
  testWidgets('NutrientResultsScreen renders summary and categories', (WidgetTester tester) async {
    tester.view.physicalSize = const Size(1200, 900);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());

    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          vegetableNutrientProfileAsyncProvider.overrideWith((ref, slug) => null),
        ],
        child: const MaterialApp(
          home: Scaffold(body: NutrientResultsScreen()),
        ),
      ),
    );
    await tester.pumpAndSettle();

    // Verify Title and Subtitle
    expect(find.text('Carrot'), findsWidgets);
    expect(find.text('Vitamins'), findsOneWidget);
    expect(find.text('Minerals & Electrolytes'), findsOneWidget);
    expect(find.text('Dietary Fibre & Bioactives'), findsOneWidget);
    expect(find.text('Estimate by Peel Weight'), findsOneWidget);
  });

  testWidgets('VitaminDetailsScreen renders essential vitamins guide', (WidgetTester tester) async {
    tester.view.physicalSize = const Size(1200, 900);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());

    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          vitaminsAsyncProvider.overrideWith((ref) => [
            const NutrientMasterItem(
              id: 1,
              code: 'vit_a',
              nameEn: 'Vitamin A / Carotenoids',
              nameTa: 'வைட்டமின் ஏ',
              category: 'vitamin',
              standardUnit: 'mcg',
              biologicalRoleEn: 'Vision and mucosal immunity',
              biologicalRoleTa: 'பார்வைத்திறன்',
            ),
          ]),
        ],
        child: const MaterialApp(
          home: VitaminDetailsScreen(),
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Vitamin Reference Guide (13 Essential)'), findsOneWidget);
    expect(find.textContaining('Scientific Notice'), findsOneWidget);
    expect(find.text('Vitamin A / Carotenoids'), findsOneWidget);
  });

  testWidgets('MineralDetailsScreen renders essential minerals guide', (WidgetTester tester) async {
    tester.view.physicalSize = const Size(1200, 900);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());

    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          mineralsAsyncProvider.overrideWith((ref) => [
            const NutrientMasterItem(
              id: 2,
              code: 'calcium',
              nameEn: 'Calcium (Ca)',
              nameTa: 'கால்சியம்',
              category: 'mineral',
              standardUnit: 'mg',
              biologicalRoleEn: 'Bone matrix and structural integrity',
              biologicalRoleTa: 'எலும்பு வளர்ச்சி',
            ),
          ]),
        ],
        child: const MaterialApp(
          home: MineralDetailsScreen(),
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Mineral & Electrolyte Guide (10 Essential)'), findsOneWidget);
    expect(find.text('Calcium (Ca)'), findsOneWidget);
  });
}
