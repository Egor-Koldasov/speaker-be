import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:vocabo/models/test_case.dart';
import '../main.dart';

class TestService {
  List<TestCase> _testCases = [];
  
  Future<void> initialize() async {
    try {
      logger.i('Loading test cases');
      final jsonString = await rootBundle.loadString('assets/test_data/test_cases.json');
      final List<dynamic> jsonList = json.decode(jsonString);
      _testCases = jsonList.map((json) => TestCase.fromJson(json)).toList();
      logger.i('Loaded ${_testCases.length} test cases');
    } catch (e) {
      logger.e('Failed to load test cases: $e');
      // Provide fallback test cases
      _testCases = [
        const TestCase(
          id: 'english_to_spanish',
          name: 'English to Spanish Translation',
          description: 'Basic translation of an English sentence to Spanish',
          inputText: 'Hello, how are you today? I would like to learn Spanish.',
          languageFrom: 'English',
          languageTo: 'Spanish',
          expectedKeywords: ['Hola', 'cómo', 'estás', 'hoy', 'aprender', 'español'],
          expectedOutput: '¡Hola! ¿Cómo estás hoy? Me gustaría aprender español.',
        ),
      ];
    }
  }
  
  List<TestCase> getAllTestCases() {
    return _testCases;
  }
  
  TestCase? getTestCaseById(String id) {
    try {
      return _testCases.firstWhere((test) => test.id == id);
    } catch (e) {
      logger.e('Test case not found: $id');
      return null;
    }
  }
  
  double calculateAccuracy(TestCase testCase, String output) {
    // Simple keyword-based accuracy calculation
    if (testCase.expectedKeywords.isEmpty) {
      return 1.0; // No keywords to check
    }
    
    final normalizedOutput = output.toLowerCase();
    int matchCount = 0;
    
    for (final keyword in testCase.expectedKeywords) {
      if (normalizedOutput.contains(keyword.toLowerCase())) {
        matchCount++;
      }
    }
    
    return matchCount / testCase.expectedKeywords.length;
  }
}