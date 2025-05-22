import 'package:flutter_blue_plus/flutter_blue_plus.dart';

class BLEController {
  BluetoothDevice? _device;
  BluetoothCharacteristic? _characteristic;

  Future<void> connectToRobot({String deviceName = "MyRobot"}) async {
    FlutterBluePlus.startScan(timeout: Duration(seconds: 4));
    FlutterBluePlus.scanResults.listen((results) async {
      for (ScanResult r in results) {
        if (r.device.name == deviceName) {
          await FlutterBluePlus.stopScan();
          _device = r.device;
          await _device!.connect();

          List<BluetoothService> services = await _device!.discoverServices();
          for (BluetoothService s in services) {
            for (BluetoothCharacteristic c in s.characteristics) {
              if (c.properties.write) {
                _characteristic = c;
                return;
              }
            }
          }
        }
      }
    });
  }

  Future<void> sendCommand(String command) async {
    if (_characteristic != null) {
      await _characteristic!.write(command.codeUnits);
    }
  }

  void disconnect() {
    _device?.disconnect();
  }

  bool get isConnected => _device != null;
}
