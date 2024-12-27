import { schemaObject } from "./_util/schemaObject";

export default schemaObject(
  {
    ModelBase: {
      $ref: "./types/LensModelBase.json",
    },
    User: {
      $ref: "./lens-models/User.json",
    },
    UserSettings: {
      $ref: "./lens-models/UserSettings.json",
    },
    SignUpCode: {
      $ref: "./lens-models/SignUpCode.json",
    },
    SessionToken: {
      $ref: "./lens-models/SessionToken.json",
    },
  },
  {
    title: "LensModels",
  }
);
