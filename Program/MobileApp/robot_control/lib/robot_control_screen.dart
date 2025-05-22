import 'package:flutter/material.dart';
import 'ble_controller.dart';

class RobotControlScreen extends StatefulWidget {
  const RobotControlScreen({super.key});

  @override
  State<RobotControlScreen> createState() => _RobotControlScreenState();
}

class _RobotControlScreenState extends State<RobotControlScreen> {
  final BLEController _bleController = BLEController();
  bool _isConnected = false;

  @override
  void initState() {
    super.initState();
    connectToBLE();
  }

  Future<void> connectToBLE() async {
    await _bleController.connectToRobot();
    setState(() {
      _isConnected = _bleController.isConnected;
    });
  }

  void sendCommand(String cmd) {
    if (_isConnected) {
      _bleController.sendCommand(cmd);
    }
  }

  @override
  void dispose() {
    _bleController.disconnect();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.lightBlueAccent, Colors.greenAccent],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(12.0),
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    _modeButton("AUTOMATIC"),
                    Column(
                      children: [
                        const Text(
                          "Stock",
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                            backgroundColor: Colors.black,
                            color: Colors.white,
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 8,
                          ),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            border: Border.all(color: Colors.black, width: 2),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: const Text(
                            "999",
                            style: TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
                    _modeButton("MANUAL"),
                  ],
                ),
                const SizedBox(height: 20),
                Expanded(
                  child: Row(
                    children: [
                      // Directional pad (left)
                      Expanded(
                        flex: 2,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            _arrowButton(Icons.arrow_drop_up, "UP"),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                _arrowButton(Icons.arrow_left, "LEFT"),
                                const SizedBox(width: 30),
                                _arrowButton(Icons.arrow_right, "RIGHT"),
                              ],
                            ),
                            _arrowButton(Icons.arrow_drop_down, "DOWN"),
                          ],
                        ),
                      ),
                      // Center Control Buttons
                      Expanded(
                        flex: 1,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Text(
                              "CONTROL",
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 18,
                              ),
                            ),
                            const SizedBox(height: 10),
                            _controlButton("ON", Colors.green),
                            const SizedBox(height: 10),
                            _controlButton("OFF", Colors.red),
                          ],
                        ),
                      ),
                      // Right Action Buttons
                      Expanded(
                        flex: 2,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            _actionButton("CAPIT"),
                            const SizedBox(height: 20),
                            _actionButton("LEPAS"),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _modeButton(String label) {
    return GestureDetector(
      onTap: () => sendCommand(label.toUpperCase()),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        decoration: BoxDecoration(
          color: Colors.black,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(
          label,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }

  Widget _arrowButton(IconData icon, String command) {
    return IconButton(
      icon: Icon(icon, size: 40, color: Colors.black),
      onPressed: () => sendCommand(command),
    );
  }

  Widget _controlButton(String label, Color color) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
      ),
      onPressed: () => sendCommand(label.toUpperCase()),
      child: Text(
        label,
        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget _actionButton(String label) {
    return GestureDetector(
      onTap: () => sendCommand(label.toUpperCase()),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.grey.shade400,
          borderRadius: BorderRadius.circular(20),
        ),
        padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 18),
        child: Text(
          label,
          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
    );
  }
}
