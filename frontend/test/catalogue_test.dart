import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_peel_ai/screens/catalogue/vegetable_catalogue_screen.dart';
import 'package:smart_peel_ai/providers/app_providers.dart';
import 'package:smart_peel_ai/providers/vegetable_providers.dart';

void main() {
  testWidgets('VegetableCatalogueScreen renders 50 vegetables and reactive search', (WidgetTester tester) async {
    tester.view.physicalSize = const Size(1200, 900);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());

    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          vegetablesListAsyncProvider.overrideWith((ref) => initialCatalogue),
        ],
        child: const MaterialApp(
          home: VegetableCatalogueScreen(),
        ),
      ),
    );
    await tester.pumpAndSettle();

    // Verify Title and Subtitle
    expect(find.text('Vegetable Master Catalogue'), findsOneWidget);
    expect(find.text('Carrot'), findsWidgets);
    expect(find.text('Potato'), findsWidgets);
    expect(find.text('AI Ready'), findsWidgets);

    // Enter search query "carrot"
    final searchField = find.byType(TextField);
    expect(searchField, findsOneWidget);

    await tester.enterText(searchField, 'carrot');
    await tester.pumpAndSettle();

    // Verify carrot is visible and potato is filtered out
    expect(find.text('Carrot'), findsOneWidget);
    expect(find.text('Potato'), findsNothing);

    // Clear search
    final clearButton = find.byIcon(Icons.clear);
    expect(clearButton, findsOneWidget);
    await tester.tap(clearButton);
    await tester.pumpAndSettle();

    // Potato should be visible again
    expect(find.text('Potato'), findsWidgets);
  });
}
