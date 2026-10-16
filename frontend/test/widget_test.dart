import 'package:flutter_test/flutter_test.dart';
import 'package:smart_peel_ai/main.dart';

void main() {
  testWidgets('SmartPeelApp smoke test - verifies initial launch and title', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const SmartPeelApp());

    // Verify app title exists in appbar.
    expect(find.text('SMART PEEL AI'), findsOneWidget);

    // Verify main heading exists.
    expect(find.text('Smart Peel AI System'), findsOneWidget);
  });
}
