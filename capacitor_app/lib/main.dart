import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';
import 'ui/app.dart';

final logger = Logger(
  printer: PrettyPrinter(
    methodCount: 0,
    errorMethodCount: 5,
    lineLength: 50,
    colors: true,
    printEmojis: true,
    printTime: true,
  ),
);

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  
  logger.i('Starting Vocabo app');
  
  runApp(
    const ProviderScope(
      child: VocaboApp(),
    ),
  );
}
