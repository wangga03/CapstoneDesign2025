import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:robot_control2/screens/robot_control_screen.dart';

void main() {
  testWidgets('RobotControlScreen loads correctly', (
    WidgetTester tester,
  ) async {
    // Build the RobotControlScreen widget
    await tester.pumpWidget(const MaterialApp(home: RobotControlScreen()));

    // Verifikasi bahwa teks CONTROL muncul
    expect(find.text('CONTROL'), findsOneWidget);

    // Verifikasi bahwa tombol "CAPIT" muncul
    expect(find.text('CAPIT'), findsOneWidget);
  });
}
