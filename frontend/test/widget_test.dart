import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_peel_ai/main.dart';

void main() {
  testWidgets('SmartPeelApp launches into SplashScreen and advances to WelcomeScreen', (WidgetTester tester) async {
    // Set surface size to avoid desktop/mobile overflow during tests
    tester.view.physicalSize = const Size(1200, 900);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());

    // Build application inside ProviderScope
    await tester.pumpWidget(
      const ProviderScope(
        child: SmartPeelApp(),
      ),
    );
    await tester.pump();

    // Verify SplashScreen is loaded
    expect(find.text('SMART PEEL AI'), findsOneWidget);
    expect(find.text('Tap to Skip >'), findsOneWidget);

    // Tap to Skip
    await tester.tap(find.text('Tap to Skip >'));
    await tester.pumpAndSettle();

    // Verify WelcomeScreen loaded
    expect(find.text('Start Instant Scan'), findsOneWidget);
    expect(find.text('Browse 50 Vegetable Catalogue'), findsOneWidget);

    // Tap Start Instant Scan to enter Home Dashboard
    await tester.tap(find.text('Start Instant Scan'));
    await tester.pumpAndSettle();

    // Verify Home Dashboard loaded
    expect(find.text('Botanical Catalogue'), findsOneWidget);
    expect(find.text('Live Camera Scan'), findsOneWidget);
  });
}
