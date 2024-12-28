import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    user: {
      $ref: "../db-models/User.json",
    },
    userSettings: {
      $ref: "../db-models/UserSettings.json",
    },
  },
  {
    title: "AuthInfo",
  }
);
