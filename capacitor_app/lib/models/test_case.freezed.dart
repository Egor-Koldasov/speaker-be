// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'test_case.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

TestCase _$TestCaseFromJson(Map<String, dynamic> json) {
  return _TestCase.fromJson(json);
}

/// @nodoc
mixin _$TestCase {
  String get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  String get description => throw _privateConstructorUsedError;
  String get inputText => throw _privateConstructorUsedError;
  String get languageFrom => throw _privateConstructorUsedError;
  String get languageTo => throw _privateConstructorUsedError;
  List<String> get expectedKeywords => throw _privateConstructorUsedError;
  String? get expectedOutput => throw _privateConstructorUsedError;

  /// Serializes this TestCase to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of TestCase
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $TestCaseCopyWith<TestCase> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $TestCaseCopyWith<$Res> {
  factory $TestCaseCopyWith(TestCase value, $Res Function(TestCase) then) =
      _$TestCaseCopyWithImpl<$Res, TestCase>;
  @useResult
  $Res call({
    String id,
    String name,
    String description,
    String inputText,
    String languageFrom,
    String languageTo,
    List<String> expectedKeywords,
    String? expectedOutput,
  });
}

/// @nodoc
class _$TestCaseCopyWithImpl<$Res, $Val extends TestCase>
    implements $TestCaseCopyWith<$Res> {
  _$TestCaseCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of TestCase
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = null,
    Object? inputText = null,
    Object? languageFrom = null,
    Object? languageTo = null,
    Object? expectedKeywords = null,
    Object? expectedOutput = freezed,
  }) {
    return _then(
      _value.copyWith(
            id:
                null == id
                    ? _value.id
                    : id // ignore: cast_nullable_to_non_nullable
                        as String,
            name:
                null == name
                    ? _value.name
                    : name // ignore: cast_nullable_to_non_nullable
                        as String,
            description:
                null == description
                    ? _value.description
                    : description // ignore: cast_nullable_to_non_nullable
                        as String,
            inputText:
                null == inputText
                    ? _value.inputText
                    : inputText // ignore: cast_nullable_to_non_nullable
                        as String,
            languageFrom:
                null == languageFrom
                    ? _value.languageFrom
                    : languageFrom // ignore: cast_nullable_to_non_nullable
                        as String,
            languageTo:
                null == languageTo
                    ? _value.languageTo
                    : languageTo // ignore: cast_nullable_to_non_nullable
                        as String,
            expectedKeywords:
                null == expectedKeywords
                    ? _value.expectedKeywords
                    : expectedKeywords // ignore: cast_nullable_to_non_nullable
                        as List<String>,
            expectedOutput:
                freezed == expectedOutput
                    ? _value.expectedOutput
                    : expectedOutput // ignore: cast_nullable_to_non_nullable
                        as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$TestCaseImplCopyWith<$Res>
    implements $TestCaseCopyWith<$Res> {
  factory _$$TestCaseImplCopyWith(
    _$TestCaseImpl value,
    $Res Function(_$TestCaseImpl) then,
  ) = __$$TestCaseImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String id,
    String name,
    String description,
    String inputText,
    String languageFrom,
    String languageTo,
    List<String> expectedKeywords,
    String? expectedOutput,
  });
}

/// @nodoc
class __$$TestCaseImplCopyWithImpl<$Res>
    extends _$TestCaseCopyWithImpl<$Res, _$TestCaseImpl>
    implements _$$TestCaseImplCopyWith<$Res> {
  __$$TestCaseImplCopyWithImpl(
    _$TestCaseImpl _value,
    $Res Function(_$TestCaseImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of TestCase
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? description = null,
    Object? inputText = null,
    Object? languageFrom = null,
    Object? languageTo = null,
    Object? expectedKeywords = null,
    Object? expectedOutput = freezed,
  }) {
    return _then(
      _$TestCaseImpl(
        id:
            null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                    as String,
        name:
            null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                    as String,
        description:
            null == description
                ? _value.description
                : description // ignore: cast_nullable_to_non_nullable
                    as String,
        inputText:
            null == inputText
                ? _value.inputText
                : inputText // ignore: cast_nullable_to_non_nullable
                    as String,
        languageFrom:
            null == languageFrom
                ? _value.languageFrom
                : languageFrom // ignore: cast_nullable_to_non_nullable
                    as String,
        languageTo:
            null == languageTo
                ? _value.languageTo
                : languageTo // ignore: cast_nullable_to_non_nullable
                    as String,
        expectedKeywords:
            null == expectedKeywords
                ? _value._expectedKeywords
                : expectedKeywords // ignore: cast_nullable_to_non_nullable
                    as List<String>,
        expectedOutput:
            freezed == expectedOutput
                ? _value.expectedOutput
                : expectedOutput // ignore: cast_nullable_to_non_nullable
                    as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$TestCaseImpl implements _TestCase {
  const _$TestCaseImpl({
    required this.id,
    required this.name,
    required this.description,
    required this.inputText,
    required this.languageFrom,
    required this.languageTo,
    final List<String> expectedKeywords = const [],
    this.expectedOutput,
  }) : _expectedKeywords = expectedKeywords;

  factory _$TestCaseImpl.fromJson(Map<String, dynamic> json) =>
      _$$TestCaseImplFromJson(json);

  @override
  final String id;
  @override
  final String name;
  @override
  final String description;
  @override
  final String inputText;
  @override
  final String languageFrom;
  @override
  final String languageTo;
  final List<String> _expectedKeywords;
  @override
  @JsonKey()
  List<String> get expectedKeywords {
    if (_expectedKeywords is EqualUnmodifiableListView)
      return _expectedKeywords;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_expectedKeywords);
  }

  @override
  final String? expectedOutput;

  @override
  String toString() {
    return 'TestCase(id: $id, name: $name, description: $description, inputText: $inputText, languageFrom: $languageFrom, languageTo: $languageTo, expectedKeywords: $expectedKeywords, expectedOutput: $expectedOutput)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$TestCaseImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.inputText, inputText) ||
                other.inputText == inputText) &&
            (identical(other.languageFrom, languageFrom) ||
                other.languageFrom == languageFrom) &&
            (identical(other.languageTo, languageTo) ||
                other.languageTo == languageTo) &&
            const DeepCollectionEquality().equals(
              other._expectedKeywords,
              _expectedKeywords,
            ) &&
            (identical(other.expectedOutput, expectedOutput) ||
                other.expectedOutput == expectedOutput));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    name,
    description,
    inputText,
    languageFrom,
    languageTo,
    const DeepCollectionEquality().hash(_expectedKeywords),
    expectedOutput,
  );

  /// Create a copy of TestCase
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$TestCaseImplCopyWith<_$TestCaseImpl> get copyWith =>
      __$$TestCaseImplCopyWithImpl<_$TestCaseImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$TestCaseImplToJson(this);
  }
}

abstract class _TestCase implements TestCase {
  const factory _TestCase({
    required final String id,
    required final String name,
    required final String description,
    required final String inputText,
    required final String languageFrom,
    required final String languageTo,
    final List<String> expectedKeywords,
    final String? expectedOutput,
  }) = _$TestCaseImpl;

  factory _TestCase.fromJson(Map<String, dynamic> json) =
      _$TestCaseImpl.fromJson;

  @override
  String get id;
  @override
  String get name;
  @override
  String get description;
  @override
  String get inputText;
  @override
  String get languageFrom;
  @override
  String get languageTo;
  @override
  List<String> get expectedKeywords;
  @override
  String? get expectedOutput;

  /// Create a copy of TestCase
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$TestCaseImplCopyWith<_$TestCaseImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

TestResult _$TestResultFromJson(Map<String, dynamic> json) {
  return _TestResult.fromJson(json);
}

/// @nodoc
mixin _$TestResult {
  String get testCaseId => throw _privateConstructorUsedError;
  String get modelName => throw _privateConstructorUsedError;
  String get outputText => throw _privateConstructorUsedError;
  int get responseTimeMs => throw _privateConstructorUsedError;
  DateTime get timestamp => throw _privateConstructorUsedError;
  double? get accuracy => throw _privateConstructorUsedError;
  String? get errorMessage => throw _privateConstructorUsedError;

  /// Serializes this TestResult to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of TestResult
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $TestResultCopyWith<TestResult> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $TestResultCopyWith<$Res> {
  factory $TestResultCopyWith(
    TestResult value,
    $Res Function(TestResult) then,
  ) = _$TestResultCopyWithImpl<$Res, TestResult>;
  @useResult
  $Res call({
    String testCaseId,
    String modelName,
    String outputText,
    int responseTimeMs,
    DateTime timestamp,
    double? accuracy,
    String? errorMessage,
  });
}

/// @nodoc
class _$TestResultCopyWithImpl<$Res, $Val extends TestResult>
    implements $TestResultCopyWith<$Res> {
  _$TestResultCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of TestResult
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? testCaseId = null,
    Object? modelName = null,
    Object? outputText = null,
    Object? responseTimeMs = null,
    Object? timestamp = null,
    Object? accuracy = freezed,
    Object? errorMessage = freezed,
  }) {
    return _then(
      _value.copyWith(
            testCaseId:
                null == testCaseId
                    ? _value.testCaseId
                    : testCaseId // ignore: cast_nullable_to_non_nullable
                        as String,
            modelName:
                null == modelName
                    ? _value.modelName
                    : modelName // ignore: cast_nullable_to_non_nullable
                        as String,
            outputText:
                null == outputText
                    ? _value.outputText
                    : outputText // ignore: cast_nullable_to_non_nullable
                        as String,
            responseTimeMs:
                null == responseTimeMs
                    ? _value.responseTimeMs
                    : responseTimeMs // ignore: cast_nullable_to_non_nullable
                        as int,
            timestamp:
                null == timestamp
                    ? _value.timestamp
                    : timestamp // ignore: cast_nullable_to_non_nullable
                        as DateTime,
            accuracy:
                freezed == accuracy
                    ? _value.accuracy
                    : accuracy // ignore: cast_nullable_to_non_nullable
                        as double?,
            errorMessage:
                freezed == errorMessage
                    ? _value.errorMessage
                    : errorMessage // ignore: cast_nullable_to_non_nullable
                        as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$TestResultImplCopyWith<$Res>
    implements $TestResultCopyWith<$Res> {
  factory _$$TestResultImplCopyWith(
    _$TestResultImpl value,
    $Res Function(_$TestResultImpl) then,
  ) = __$$TestResultImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String testCaseId,
    String modelName,
    String outputText,
    int responseTimeMs,
    DateTime timestamp,
    double? accuracy,
    String? errorMessage,
  });
}

/// @nodoc
class __$$TestResultImplCopyWithImpl<$Res>
    extends _$TestResultCopyWithImpl<$Res, _$TestResultImpl>
    implements _$$TestResultImplCopyWith<$Res> {
  __$$TestResultImplCopyWithImpl(
    _$TestResultImpl _value,
    $Res Function(_$TestResultImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of TestResult
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? testCaseId = null,
    Object? modelName = null,
    Object? outputText = null,
    Object? responseTimeMs = null,
    Object? timestamp = null,
    Object? accuracy = freezed,
    Object? errorMessage = freezed,
  }) {
    return _then(
      _$TestResultImpl(
        testCaseId:
            null == testCaseId
                ? _value.testCaseId
                : testCaseId // ignore: cast_nullable_to_non_nullable
                    as String,
        modelName:
            null == modelName
                ? _value.modelName
                : modelName // ignore: cast_nullable_to_non_nullable
                    as String,
        outputText:
            null == outputText
                ? _value.outputText
                : outputText // ignore: cast_nullable_to_non_nullable
                    as String,
        responseTimeMs:
            null == responseTimeMs
                ? _value.responseTimeMs
                : responseTimeMs // ignore: cast_nullable_to_non_nullable
                    as int,
        timestamp:
            null == timestamp
                ? _value.timestamp
                : timestamp // ignore: cast_nullable_to_non_nullable
                    as DateTime,
        accuracy:
            freezed == accuracy
                ? _value.accuracy
                : accuracy // ignore: cast_nullable_to_non_nullable
                    as double?,
        errorMessage:
            freezed == errorMessage
                ? _value.errorMessage
                : errorMessage // ignore: cast_nullable_to_non_nullable
                    as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$TestResultImpl implements _TestResult {
  const _$TestResultImpl({
    required this.testCaseId,
    required this.modelName,
    required this.outputText,
    required this.responseTimeMs,
    required this.timestamp,
    this.accuracy,
    this.errorMessage,
  });

  factory _$TestResultImpl.fromJson(Map<String, dynamic> json) =>
      _$$TestResultImplFromJson(json);

  @override
  final String testCaseId;
  @override
  final String modelName;
  @override
  final String outputText;
  @override
  final int responseTimeMs;
  @override
  final DateTime timestamp;
  @override
  final double? accuracy;
  @override
  final String? errorMessage;

  @override
  String toString() {
    return 'TestResult(testCaseId: $testCaseId, modelName: $modelName, outputText: $outputText, responseTimeMs: $responseTimeMs, timestamp: $timestamp, accuracy: $accuracy, errorMessage: $errorMessage)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$TestResultImpl &&
            (identical(other.testCaseId, testCaseId) ||
                other.testCaseId == testCaseId) &&
            (identical(other.modelName, modelName) ||
                other.modelName == modelName) &&
            (identical(other.outputText, outputText) ||
                other.outputText == outputText) &&
            (identical(other.responseTimeMs, responseTimeMs) ||
                other.responseTimeMs == responseTimeMs) &&
            (identical(other.timestamp, timestamp) ||
                other.timestamp == timestamp) &&
            (identical(other.accuracy, accuracy) ||
                other.accuracy == accuracy) &&
            (identical(other.errorMessage, errorMessage) ||
                other.errorMessage == errorMessage));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    testCaseId,
    modelName,
    outputText,
    responseTimeMs,
    timestamp,
    accuracy,
    errorMessage,
  );

  /// Create a copy of TestResult
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$TestResultImplCopyWith<_$TestResultImpl> get copyWith =>
      __$$TestResultImplCopyWithImpl<_$TestResultImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$TestResultImplToJson(this);
  }
}

abstract class _TestResult implements TestResult {
  const factory _TestResult({
    required final String testCaseId,
    required final String modelName,
    required final String outputText,
    required final int responseTimeMs,
    required final DateTime timestamp,
    final double? accuracy,
    final String? errorMessage,
  }) = _$TestResultImpl;

  factory _TestResult.fromJson(Map<String, dynamic> json) =
      _$TestResultImpl.fromJson;

  @override
  String get testCaseId;
  @override
  String get modelName;
  @override
  String get outputText;
  @override
  int get responseTimeMs;
  @override
  DateTime get timestamp;
  @override
  double? get accuracy;
  @override
  String? get errorMessage;

  /// Create a copy of TestResult
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$TestResultImplCopyWith<_$TestResultImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
