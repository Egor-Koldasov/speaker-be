import { schemaChatOutput } from "../_util/schemaChatOutput";

export default schemaChatOutput(
  {
    outputData: {
      $ref: "./ChatOutputDataDefineTerm.json",
    },
  },
  {
    title: "ChatOutputDefineTerm",
  }
);
