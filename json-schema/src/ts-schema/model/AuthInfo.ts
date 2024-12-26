import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    user: {
      $ref: "../lens-models/User.json",
    },
    userSettings: {
      $ref: "../lens-models/UserSettings.json",
    },
  },
  {
    title: "AuthInfo",
  }
);
