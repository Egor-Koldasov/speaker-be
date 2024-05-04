import { schema } from "../_util/schema";

export default schema({
  title: "ErrorName",
  type: "string",
  description: "The code name of the error.",
  enum: [
    "Unknown",
    "Internal",
    "Ai_CreateCompletion",
    "AI_ResponseUnmarshal",
    "JsonSchema_MessageInput",
    "JsonSchema_MessageOutput",
    "NotFound_MessageName",
    "FromAi_Critical",
  ],
});
