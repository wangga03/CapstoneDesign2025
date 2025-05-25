import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:robot_control/main.dart';

void main() {
  final _ = Colors.transparent; // ← ini pakai 1 properti dari material.dart

  testWidgets('Robot controller UI test', (WidgetTester tester) async {
    await tester.pumpWidget(RobotControllerApp());

    expect(find.text('Maju'), findsOneWidget);
    expect(find.text('Mundur'), findsOneWidget);
  });
}
