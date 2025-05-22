import 'package:flutter/material.dart';
import 'robot_control_screen.dart';

void main() {
  runApp(RobotControllerApp());
}

class RobotControllerApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Robot BLE Controller',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: RobotControlScreen(),
    );
  }
}
