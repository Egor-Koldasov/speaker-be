package fieldgenprompt

import (
	"api-go/pkg/aichatprompt"
	"api-go/pkg/genjsonschema"
	"fmt"
	"strings"
)

// NewFieldGenPrompt creates a text-based prompt that merges the given
// CardConfig (parent) with a FieldConfig (child). It combines parameter
// definitions from both the CardConfig and FieldConfig, splitting them into
// definitions and actual values.
func NewFieldGenPrompt(
	fieldConfig genjsonschema.FieldConfig,
	cardConfig genjsonschema.CardConfig,
	// User-provided parameter values for the Card
	cardParamValues map[string]string,
	// User-provided parameter values for the Field
	fieldParamValues map[string]string,
) []aichatprompt.AiChatPrompt {
	developerPrompt := aichatprompt.AiChatPrompt{
		Role: aichatprompt.AiChatProptRoleDeveloper,
		Text: `
You are a dedicated AI component designed to generate precise, standalone content for a specific field within a structured card document.

Application Architecture:
- A CardConfig is created by the user to provide high-level background context about a domain or scenario.
- A FieldConfig is created for each individual field of the card. Each FieldConfig contains specific, user-defined instructions for generating one particular field.
- Multiple AI tasks run in parallel—each processing a separate FieldConfig for the same CardConfig. Your task is to generate the output for a single field only, using the CardConfig solely as background context.

Your Role:
- Process the combined input by using the CardConfig as supplementary context and strictly following the instructions in your assigned FieldConfig.
- Ignore any details in the CardConfig that are not explicitly referenced in your FieldConfig.
- Do not produce output that aggregates or overlaps with outputs of other parallel tasks; focus solely on your specific field.
- Do not engage in conversational behavior or simulate a chat. Your output is final and will be used directly as the card's documented value.

Rules:
1. Follow the FieldConfig instructions exactly to generate the output for one field.
2. Use the CardConfig only as background context.
3. Do not include any extra details, commentary, or embellishments beyond what the FieldConfig specifies.
4. Do not simulate a conversation or ask clarifying questions—produce a final, complete output.
5. Output must be in plain text exactly as requested.

Follow these rules precisely to ensure that your final answer is strictly aligned with the specific field instructions and is suitable to be used directly as the card's documented value.
Do not engage in chatting and do not explain your answer. Respond with a pure and isolated answer in a programmatic manner without any additional commentary.
`,
	}

	// Combine card and field parameter definitions.
	combinedDefs := append(cardConfig.PromptParameterDefinitions, fieldConfig.PromptParameterDefinitions...)

	// Combine user-supplied parameter values; field values override card values if duplicate.
	combinedValues := make(map[string]string)
	for k, v := range cardParamValues {
		combinedValues[k] = v
	}
	for k, v := range fieldParamValues {
		combinedValues[k] = v
	}

	// Helper function to format parameter definitions.
	formatParamDefinitions := func(defs []genjsonschema.PromptParameterDefinition) string {
		if len(defs) == 0 {
			return "None\n"
		}
		var sb strings.Builder
		for _, d := range defs {
			sb.WriteString(fmt.Sprintf("- Name: %s\n  Description: %s\n\n", d.Name, d.ParameterDescription))
		}
		return sb.String()
	}

	// Helper function to format parameter values.
	formatParamValues := func(defs []genjsonschema.PromptParameterDefinition, values map[string]string) string {
		if len(defs) == 0 {
			return "None\n"
		}
		var sb strings.Builder
		for _, d := range defs {
			if val, ok := values[d.Name]; ok && val != "" {
				sb.WriteString(fmt.Sprintf("- Name: %s\n  Value: %s\n\n", d.Name, val))
			} else {
				sb.WriteString(fmt.Sprintf("- Name: %s\n  Value: (No user value provided)\n\n", d.Name))
			}
		}
		return sb.String()
	}

	paramDefsStr := formatParamDefinitions(combinedDefs)
	paramValuesStr := formatParamValues(combinedDefs, combinedValues)

	// Build the user-facing prompt with updated ordering:
	// Field parameter definitions come before the field prompt.
	userMsg := fmt.Sprintf(`
=== CARD CONFIG (Context) ===
- Card ID: %s
- Card Name: %s
- Card Prompt (Context Only): %q

=== PARAMETERS DEFINITIONS ===
%s

=== FIELD CONFIG (Instructions) ===
- Field ID: %s
- Field Name: %s
- Field Prompt (AI Instructions): %q
- Value Type: %s

=== PARAMETERS VALUES ===
%s

=== USER REQUEST ===
1. Use the Card Prompt above solely as context or background.
2. Follow the Field Prompt as your main instructions for generating the final text response.
3. Incorporate the parameter definitions and use the provided parameter values as applicable.
4. Produce your answer in plain text.
`,
		cardConfig.Id,
		cardConfig.Name,
		cardConfig.Prompt,
		paramDefsStr,
		fieldConfig.Id,
		fieldConfig.Name,
		fieldConfig.Prompt,
		fieldConfig.ValueType,
		paramValuesStr,
	)

	userPrompt := aichatprompt.AiChatPrompt{
		Role: aichatprompt.AiChatProptRoleUser,
		Text: strings.TrimSpace(userMsg),
	}

	fieldGenPrompts := []aichatprompt.AiChatPrompt{
		developerPrompt,
		userPrompt,
	}

	return fieldGenPrompts
}
