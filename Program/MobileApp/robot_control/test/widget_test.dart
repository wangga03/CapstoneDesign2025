import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:robot_control/main.dart'; // Benar, karena class ada di sini

void main() {
  testWidgets('Robot controller UI test', (WidgetTester tester) async {
    await tester.pumpWidget(RobotControllerApp());

    // Verifikasi tombol-tombol ada di tampilan
    expect(find.text('Maju'), findsOneWidget);
    expect(find.text('Mundur'), findsOneWidget);
  });
}
