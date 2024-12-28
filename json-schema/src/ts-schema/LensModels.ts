import { schemaObject } from "./_util/schemaObject";

export default schemaObject(
  {
    LensCardConfig: {
      $ref: "./lens-models/LensCardConfig.json",
    },
    LensCardValue: {
      $ref: "./lens-models/LensCardValue.json",
    },
  },
  {
    title: "LensModels",
  }
);
