import 'package:flutter_test/flutter_test.dart';
import 'package:unit3_activities_app/main.dart';

void main() {
  testWidgets('Unit3ActivitiesApp smoke test and title verification', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const Unit3ActivitiesApp());

    // Verify that the title appears in the AppBar
    expect(find.text('PMDM DAM2 • Prácticas Unit 3'), findsOneWidget);

    // Verify that the first activity card is present
    expect(find.text('3.1 Contador Extendido & Widgets'), findsOneWidget);
  });
}
