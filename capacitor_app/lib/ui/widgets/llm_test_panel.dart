import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:vocabo/core/providers.dart';
import 'package:vocabo/models/test_case.dart';
import 'package:vocabo/services/llm_service.dart';
import '../../main.dart';

class LlmTestPanel extends ConsumerWidget {
  const LlmTestPanel({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final testCaseId = ref.watch(selectedTestCaseIdProvider);
    final testCase = ref.watch(selectedTestCaseProvider);
    final selectedModel = ref.watch(selectedModelProvider);
    final isProcessing = ref.watch(isProcessingProvider);
    final currentResult = ref.watch(currentTestResultProvider);
    
    return Card(
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Text('Select Test Case:', style: TextStyle(fontWeight: FontWeight.bold)),
                const SizedBox(width: 16),
                Expanded(
                  child: DropdownButton<String>(
                    isExpanded: true,
                    value: testCaseId,
                    items: [
                      'english_to_spanish',
                      'english_to_french',
                      'word_definition',
                      'grammar_correction',
                    ].map((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(value.replaceAll('_', ' ').toUpperCase()),
                      );
                    }).toList(),
                    onChanged: (value) {
                      if (value != null) {
                        ref.read(selectedTestCaseIdProvider.notifier).state = value;
                      }
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                const Text('Select LLM Model:', style: TextStyle(fontWeight: FontWeight.bold)),
                const SizedBox(width: 16),
                Expanded(
                  child: DropdownButton<String>(
                    isExpanded: true,
                    value: selectedModel,
                    items: [
                      'Not selected',
                      'DeepSeek-Lite',
                      'Phi-3-mini',
                      'Gemma-2B',
                      'Qwen-1.5',
                    ].map((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(value),
                      );
                    }).toList(),
                    onChanged: isProcessing 
                      ? null 
                      : (value) {
                          if (value != null) {
                            ref.read(selectedModelProvider.notifier).state = value;
                          }
                        },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 32),
            const Text('Test Input:', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.grey.shade200,
                borderRadius: BorderRadius.circular(8),
              ),
              width: double.infinity,
              child: Text(
                testCase?.inputText ?? 'Loading...',
                style: const TextStyle(fontFamily: 'monospace'),
              ),
            ),
            const SizedBox(height: 24),
            Center(
              child: ElevatedButton(
                onPressed: isProcessing || selectedModel == 'Not selected'
                  ? null
                  : () => _runTest(ref, context),
                child: isProcessing 
                  ? const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        SizedBox(
                          width: 16,
                          height: 16, 
                          child: CircularProgressIndicator(strokeWidth: 2),
                        ),
                        SizedBox(width: 8),
                        Text('Processing...'),
                      ],
                    )
                  : const Text('Run Test'),
              ),
            ),
            const SizedBox(height: 24),
            const Text('Results:', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Expanded(
              child: Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.grey.shade300),
                ),
                width: double.infinity,
                child: currentResult != null
                  ? SingleChildScrollView(
                      child: Text(currentResult.outputText),
                    )
                  : const Center(
                      child: Text('No results yet. Run a test to see output.'),
                    ),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Performance Metrics:', style: TextStyle(fontWeight: FontWeight.bold)),
                Row(
                  children: [
                    const Icon(Icons.timer, size: 16),
                    const SizedBox(width: 4),
                    const Text('Response time: '),
                    Text(
                      currentResult != null 
                        ? '${currentResult.responseTimeMs} ms' 
                        : '-- ms',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              ],
            ),
            if (currentResult?.accuracy != null) ...[
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Accuracy:', style: TextStyle(fontWeight: FontWeight.bold)),
                  Text(
                    '${(currentResult!.accuracy! * 100).toStringAsFixed(1)}%',
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }
  
  void _runTest(WidgetRef ref, BuildContext context) async {
    final testCase = ref.read(selectedTestCaseProvider);
    final selectedModel = ref.read(selectedModelProvider);
    
    if (testCase == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Test case not found')),
      );
      return;
    }
    
    ref.read(isProcessingProvider.notifier).state = true;
    
    try {
      final llmService = await ref.read(llmServiceProvider(selectedModel).future);
      
      final startTime = DateTime.now();
      final result = await llmService.processTestCase(testCase);
      final endTime = DateTime.now();
      
      final elapsedMs = endTime.difference(startTime).inMilliseconds;
      
      // Update with actual response time
      final updatedResult = TestResult(
        testCaseId: result.testCaseId,
        modelName: result.modelName,
        outputText: result.outputText,
        responseTimeMs: elapsedMs,
        timestamp: result.timestamp,
        accuracy: result.accuracy,
        errorMessage: result.errorMessage,
      );
      
      // Update state
      ref.read(currentTestResultProvider.notifier).state = updatedResult;
      
      // Add to history
      final currentResults = ref.read(testResultsProvider);
      ref.read(testResultsProvider.notifier).state = [...currentResults, updatedResult];
      
      logger.i('Test completed: ${testCase.id} with model $selectedModel');
    } catch (e) {
      logger.e('Error running test: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: ${e.toString()}')),
      );
    } finally {
      ref.read(isProcessingProvider.notifier).state = false;
    }
  }
}