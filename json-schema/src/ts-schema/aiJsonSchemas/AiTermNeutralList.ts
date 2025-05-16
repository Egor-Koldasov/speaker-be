import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    contextTerms: {
      type: "array",
      description:
        "A list of terms extracted from the text, converted to their neutral grammatical forms",
      items: {
        $ref: "./AiContextTerm.json",
      },
    },
  },
  {
    title: "AiTermNeutralList",
    description:
      "A list of terms extracted from text, with each term converted to its neutral grammatical form",
  }
);
