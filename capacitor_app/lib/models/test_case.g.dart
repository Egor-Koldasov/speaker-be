// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'test_case.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$TestCaseImpl _$$TestCaseImplFromJson(Map<String, dynamic> json) =>
    _$TestCaseImpl(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String,
      inputText: json['inputText'] as String,
      languageFrom: json['languageFrom'] as String,
      languageTo: json['languageTo'] as String,
      expectedKeywords:
          (json['expectedKeywords'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          const [],
      expectedOutput: json['expectedOutput'] as String?,
    );

Map<String, dynamic> _$$TestCaseImplToJson(_$TestCaseImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'inputText': instance.inputText,
      'languageFrom': instance.languageFrom,
      'languageTo': instance.languageTo,
      'expectedKeywords': instance.expectedKeywords,
      'expectedOutput': instance.expectedOutput,
    };

_$TestResultImpl _$$TestResultImplFromJson(Map<String, dynamic> json) =>
    _$TestResultImpl(
      testCaseId: json['testCaseId'] as String,
      modelName: json['modelName'] as String,
      outputText: json['outputText'] as String,
      responseTimeMs: (json['responseTimeMs'] as num).toInt(),
      timestamp: DateTime.parse(json['timestamp'] as String),
      accuracy: (json['accuracy'] as num?)?.toDouble(),
      errorMessage: json['errorMessage'] as String?,
    );

Map<String, dynamic> _$$TestResultImplToJson(_$TestResultImpl instance) =>
    <String, dynamic>{
      'testCaseId': instance.testCaseId,
      'modelName': instance.modelName,
      'outputText': instance.outputText,
      'responseTimeMs': instance.responseTimeMs,
      'timestamp': instance.timestamp.toIso8601String(),
      'accuracy': instance.accuracy,
      'errorMessage': instance.errorMessage,
    };
