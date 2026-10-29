import 'package:flutter_test/flutter_test.dart';
import 'package:leadcraft_mobile/main.dart';

void main() {
  testWidgets('LeadCraft smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const LeadCraftApp());
    expect(find.text('Mapa Leads'), findsOneWidget);
  });
}
