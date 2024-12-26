import { schemaObject } from "./_util/schemaObject";

export default schemaObject(
  {
    User: {
      $ref: "./lens-models/User.json",
    },
    UserSettings: {
      $ref: "./lens-models/UserSettings.json",
    },
    ModelBase: {
      $ref: "./types/LensModelBase.json",
    },
  },
  {
    title: "LensModels",
  }
);
