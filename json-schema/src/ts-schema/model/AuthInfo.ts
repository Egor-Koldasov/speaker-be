import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    user: {
      $ref: "../lense-models/User.json",
    },
    userSettings: {
      $ref: "../lense-models/UserSettings.json",
    },
  },
  {
    title: "AuthInfo",
  }
);
