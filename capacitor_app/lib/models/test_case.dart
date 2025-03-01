import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:json_annotation/json_annotation.dart';

part 'test_case.freezed.dart';
part 'test_case.g.dart';

@freezed
class TestCase with _$TestCase {
  const factory TestCase({
    required String id,
    required String name,
    required String description,
    required String inputText,
    required String languageFrom,
    required String languageTo,
    @Default([]) List<String> expectedKeywords,
    String? expectedOutput,
  }) = _TestCase;

  factory TestCase.fromJson(Map<String, dynamic> json) => _$TestCaseFromJson(json);
}

@freezed
class TestResult with _$TestResult {
  const factory TestResult({
    required String testCaseId,
    required String modelName,
    required String outputText,
    required int responseTimeMs,
    required DateTime timestamp,
    double? accuracy,
    String? errorMessage,
  }) = _TestResult;

  factory TestResult.fromJson(Map<String, dynamic> json) => _$TestResultFromJson(json);
}