import 'dart:async';
import 'package:vocabo/models/test_case.dart';
import '../main.dart';

abstract class LlmService {
  Future<TestResult> processTestCase(TestCase testCase);
  Future<void> initialize();
  String get modelName;
  void dispose();
}

// Mock LLM service for initial development
class MockLlmService implements LlmService {
  @override
  String get modelName => "Mock LLM";

  @override
  Future<void> initialize() async {
    logger.i('Initializing mock LLM service');
    // Simulate initialization delay
    await Future.delayed(const Duration(milliseconds: 500));
  }

  @override
  Future<TestResult> processTestCase(TestCase testCase) async {
    logger.i('Processing test case: ${testCase.id}');
    
    // Simulate processing delay
    await Future.delayed(const Duration(seconds: 2));

    // Simple mock responses based on test case ID
    final now = DateTime.now();
    String outputText;
    
    switch (testCase.id) {
      case 'english_to_spanish':
        outputText = "¡Hola! ¿Cómo estás hoy? Me gustaría aprender español.";
        break;
      case 'english_to_french':
        outputText = "J'aime voyager et explorer de nouvelles cultures. Paris est belle au printemps.";
        break;
      case 'word_definition':
        outputText = "Serendipity: The occurrence and development of events by chance in a happy or beneficial way. Example: Finding a valuable book at a yard sale by accident.";
        break;
      case 'grammar_correction':
        outputText = "She doesn't like apples. Yesterday I went to the store and bought milk.";
        break;
      default:
        outputText = "Sorry, I couldn't process this request.";
    }

    return TestResult(
      testCaseId: testCase.id,
      modelName: modelName,
      outputText: outputText,
      responseTimeMs: 2000, // Mock response time
      timestamp: now,
      accuracy: 0.95, // Mock accuracy
    );
  }

  @override
  void dispose() {
    logger.i('Disposing mock LLM service');
  }
}

// Factory to create appropriate LLM service
class LlmServiceFactory {
  static LlmService createService(String modelName) {
    // For now, we only have the mock service
    // Later we'll implement actual model integrations
    switch (modelName) {
      case 'DeepSeek-Lite':
      case 'Phi-3-mini':
      case 'Gemma-2B':
      case 'Qwen-1.5':
        return MockLlmService();
      default:
        return MockLlmService();
    }
  }
}