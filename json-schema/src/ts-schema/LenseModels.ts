import { schemaObject } from "./_util/schemaObject";

export default schemaObject(
  {
    User: {
      $ref: "./lense-models/User.json",
    },
    UserSettings: {
      $ref: "./lense-models/UserSettings.json",
    },
  },
  {
    title: "LenseModels",
  }
);
