import { schemaChatOutput } from "../_util/schemaChatOutput";

export default schemaChatOutput(
  {
    outputData: {
      $ref: "./ChatOutputDataParseTextFromForeign.json",
    },
  },
  {
    title: "ChatOutputParseTextFromForeign",
  }
);
