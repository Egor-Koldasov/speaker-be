import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:vocabo/models/test_case.dart';
import 'package:vocabo/services/llm_service.dart';
import 'package:vocabo/services/test_service.dart';

// Services
final testServiceProvider = Provider<TestService>((ref) {
  return TestService();
});

final selectedModelProvider = StateProvider<String>((ref) => 'Not selected');

final llmServiceProvider = FutureProvider.family<LlmService, String>((ref, modelName) async {
  if (modelName == 'Not selected') {
    throw Exception('No model selected');
  }
  
  final service = LlmServiceFactory.createService(modelName);
  await service.initialize();
  return service;
});

// Test Case State
final selectedTestCaseIdProvider = StateProvider<String>((ref) => 'english_to_spanish');

final selectedTestCaseProvider = Provider<TestCase?>((ref) {
  final testService = ref.watch(testServiceProvider);
  final testCaseId = ref.watch(selectedTestCaseIdProvider);
  return testService.getTestCaseById(testCaseId);
});

// Test Results
final testResultsProvider = StateProvider<List<TestResult>>((ref) => []);

final currentTestResultProvider = StateProvider<TestResult?>((ref) => null);

final isProcessingProvider = StateProvider<bool>((ref) => false);