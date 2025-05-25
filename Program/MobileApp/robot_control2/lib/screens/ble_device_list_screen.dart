import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart';
import '../BLE_controller.dart';

class BleDeviceListScreen extends StatefulWidget {
  final BLEController ble;

  const BleDeviceListScreen({super.key, required this.ble});

  @override
  State<BleDeviceListScreen> createState() => _BleDeviceListScreenState();
}

class _BleDeviceListScreenState extends State<BleDeviceListScreen> {
  @override
  void initState() {
    super.initState();
    _initializeBLE();
  }

  Future<void> _initializeBLE() async {
    await _requestPermissions();
    await FlutterBluePlus.startScan(timeout: const Duration(seconds: 4));
  }

  Future<void> _requestPermissions() async {
    await [
      Permission.bluetoothScan,
      Permission.bluetoothConnect,
      Permission.location,
    ].request();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Scan Devices"),
        leading: const Icon(Icons.bluetooth),
      ),
      body: StreamBuilder<List<ScanResult>>(
        stream: FlutterBluePlus.scanResults,
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }

          final results = snapshot.data!;
          if (results.isEmpty) {
            return const Center(child: Text("Tidak ada perangkat ditemukan"));
          }

          return ListView.separated(
            itemCount: results.length,
            separatorBuilder: (_, __) => const Divider(),
            itemBuilder: (context, index) {
              final r = results[index];
              final name = r.device.name.isNotEmpty
                  ? r.device.name
                  : '<unnamed>';
              return ListTile(
                title: Text(name),
                subtitle: Text(r.device.id.id),
                trailing: const Icon(Icons.bluetooth_connected),
                onTap: () async {
                  await FlutterBluePlus.stopScan();
                  await widget.ble.connectToDevice(r.device);
                  Navigator.pop(context);
                },
              );
            },
          );
        },
      ),
    );
  }
}
