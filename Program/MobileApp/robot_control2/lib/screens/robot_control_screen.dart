import 'package:flutter/material.dart';
import 'ble_device_list_screen.dart';
import '../BLE_controller.dart' as ble;

class RobotControlScreen extends StatefulWidget {
  const RobotControlScreen({super.key});

  @override
  State<RobotControlScreen> createState() => _RobotControlScreenState();
}

class _RobotControlScreenState extends State<RobotControlScreen> {
  final ble.BLEController _ble = ble.BLEController();

  @override
  void initState() {
    super.initState();
    _ble.connectToRobot();
  }

  void _sendCommand(String cmd) {
    print(cmd);
    _ble.sendCommand(cmd);
  }

  @override
  void dispose() {
    _ble.disconnect();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Robot Controller'),
        actions: [
          IconButton(
            icon: const Icon(Icons.bluetooth_searching),
            onPressed: () async {
              await Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) => BleDeviceListScreen(ble: _ble),
                ),
              );
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Container(
          width: double.infinity,
          height: double.infinity,
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [Color(0xFFCCE5FF), Color(0xFFE6FFF2)],
            ),
          ),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Kiri
              Expanded(
                flex: 2,
                child: Padding(
                  padding: const EdgeInsets.symmetric(
                    vertical: 24.0,
                    horizontal: 8,
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      _modeButton(
                        'AUTOMATIC',
                        () => _sendCommand('otomatis\n'),
                      ),
                      _customDPad(),
                    ],
                  ),
                ),
              ),
              // Tengah
              Expanded(
                flex: 3,
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 24.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      _stockDisplay(),
                      const Text(
                        'CONTROL',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 20,
                        ),
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          _controlButton(
                            'ON',
                            Colors.green,
                            () => _sendCommand('in\n'),
                          ),
                          const SizedBox(width: 24),
                          _controlButton(
                            'OFF',
                            Colors.red,
                            () => _sendCommand('off\n'),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
              // Kanan
              Expanded(
                flex: 2,
                child: Padding(
                  padding: const EdgeInsets.symmetric(
                    vertical: 24.0,
                    horizontal: 8,
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      _modeButton('MANUAL', () => _sendCommand('manual\n')),
                      Column(
                        children: [
                          _actionButton('CAPIT', () => _sendCommand('capit\n')),
                          const SizedBox(height: 24),
                          _actionButton('LEPAS', () => _sendCommand('lepas\n')),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _modeButton(String label, VoidCallback onPressed) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        decoration: BoxDecoration(
          color: Colors.black,
          borderRadius: BorderRadius.circular(28),
        ),
        child: Text(
          label,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
            fontSize: 14,
          ),
        ),
      ),
    );
  }

  Widget _stockDisplay() {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
          decoration: BoxDecoration(
            color: Colors.black,
            borderRadius: BorderRadius.circular(14),
          ),
          child: const Text(
            'Stock',
            style: TextStyle(color: Colors.white, fontSize: 14),
          ),
        ),
        Container(
          margin: const EdgeInsets.only(top: 4),
          width: 80,
          height: 50,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(width: 2, color: Colors.black),
          ),
          child: const Text('999', style: TextStyle(fontSize: 24)),
        ),
      ],
    );
  }

  Widget _customDPad() {
    return SizedBox(
      width: 120,
      height: 120,
      child: Stack(
        children: [
          Align(
            alignment: Alignment.topCenter,
            child: GestureDetector(
              onTap: () => _sendCommand('maju\n'),
              child: Container(width: 30, height: 50, color: Colors.black),
            ),
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: GestureDetector(
              onTap: () => _sendCommand('mundur\n'),
              child: Container(width: 30, height: 50, color: Colors.black),
            ),
          ),
          Align(
            alignment: Alignment.centerLeft,
            child: GestureDetector(
              onTap: () => _sendCommand('kiri\n'),
              child: Container(width: 50, height: 30, color: Colors.black),
            ),
          ),
          Align(
            alignment: Alignment.centerRight,
            child: GestureDetector(
              onTap: () => _sendCommand('kanan\n'),
              child: Container(width: 50, height: 30, color: Colors.black),
            ),
          ),
          Align(
            alignment: Alignment.center,
            child: Container(width: 30, height: 30, color: Colors.black),
          ),
        ],
      ),
    );
  }

  Widget _controlButton(String label, Color color, VoidCallback onPressed) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
        padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 14),
      ),
      child: Text(
        label,
        style: const TextStyle(fontSize: 16, color: Colors.white),
      ),
    );
  }

  Widget _actionButton(String label, VoidCallback onPressed) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        width: 140,
        padding: const EdgeInsets.symmetric(vertical: 18),
        decoration: BoxDecoration(
          color: Colors.grey[400],
          borderRadius: BorderRadius.circular(28),
        ),
        alignment: Alignment.center,
        child: Text(
          label,
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
        ),
      ),
    );
  }
}
