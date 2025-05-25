import 'dart:convert';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

class BLEController {
  BluetoothDevice? _device;
  BluetoothCharacteristic? _characteristic;

  // Ganti UUID ini sesuai karakteristik BLE device kamu yang mendukung write
  static const String targetCharacteristicUuid =
      "0000ffe1-0000-1000-8000-00805f9b34fb";

  Future<void> connectToDevice(BluetoothDevice device) async {
    if (!device.isConnected) {
      await device.connect(autoConnect: false);
      await Future.delayed(const Duration(seconds: 1));
    }
    _device = device;

    List<BluetoothService> services = await device.discoverServices();

    for (var service in services) {
      for (var char in service.characteristics) {
        print("🔍 Karakteristik: ${char.uuid}");
        print("    ➤ write: ${char.properties.write}");
        print("    ➤ writeNoResp: ${char.properties.writeWithoutResponse}");

        if ((char.properties.write || char.properties.writeWithoutResponse) &&
            char.uuid.toString().toLowerCase().endsWith("ffe1")) {
          _characteristic = char;
          print("✅ Karakteristik write ditemukan: ${char.uuid}");
          return;
        }
      }
    }

    throw Exception('❌ Karakteristik write yang sesuai tidak ditemukan.');
  }

  Future<void> connectToRobot() async {
    await FlutterBluePlus.startScan(timeout: const Duration(seconds: 4));
    await for (final results in FlutterBluePlus.scanResults) {
      for (final r in results) {
        if (r.device.name == 'RobotBLE') {
          await FlutterBluePlus.stopScan();
          await connectToDevice(r.device);
          return;
        }
      }
    }
    throw Exception("❌ RobotBLE tidak ditemukan.");
  }

  Future<void> sendCommand(String cmd) async {
    if (_characteristic == null) {
      print('❌ Karakteristik belum siap.');
      return;
    }

    try {
      final bytes = utf8.encode(cmd);

      if (_characteristic!.properties.writeWithoutResponse) {
        await _characteristic!.write(bytes, withoutResponse: true);
        print("📤 Perintah dikirim (tanpa response): $cmd");
      } else if (_characteristic!.properties.write) {
        await _characteristic!.write(bytes, withoutResponse: false);
        print("📤 Perintah dikirim (dengan response): $cmd");
      } else {
        print("❌ Karakteristik tidak mendukung penulisan.");
      }
    } catch (e) {
      print("❌ Gagal kirim perintah: $e");
    }
  }

  Future<void> disconnect() async {
    if (_device != null) {
      await _device!.disconnect();
      print("🔌 Terputus dari perangkat.");
    }
  }
}
