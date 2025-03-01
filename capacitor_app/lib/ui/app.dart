import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:vocabo/services/test_service.dart';
import 'package:vocabo/core/providers.dart';
import 'screens/home_screen.dart';
import 'theme/app_theme.dart';

class VocaboApp extends ConsumerStatefulWidget {
  const VocaboApp({super.key});

  @override
  ConsumerState<VocaboApp> createState() => _VocaboAppState();
}

class _VocaboAppState extends ConsumerState<VocaboApp> {
  @override
  void initState() {
    super.initState();
    _initializeServices();
  }

  Future<void> _initializeServices() async {
    final testService = ref.read(testServiceProvider);
    await testService.initialize();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Vocabo',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      routerConfig: _router,
      debugShowCheckedModeBanner: false,
    );
  }
}

final _router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
  ],
);