import { schemaObject } from "./_util/schemaObject";

export default schemaObject(
  {
    ModelBase: {
      $ref: "./db-models/DbModelBase.json",
    },
    User: {
      $ref: "./db-models/User.json",
    },
    UserSettings: {
      $ref: "./db-models/UserSettings.json",
    },
    SignUpCode: {
      $ref: "./db-models/SignUpCode.json",
    },
    SessionToken: {
      $ref: "./db-models/SessionToken.json",
    },
    CardConfig: {
      $ref: "./db-models/CardConfig.json",
    },
    FieldConfig: {
      $ref: "./db-models/FieldConfig.json",
    },
    FieldValue: {
      $ref: "./db-models/FieldValue.json",
    },
    FieldValueSet: {
      $ref: "./db-models/FieldValueSet.json",
    },
    RelCardConfigFieldConfig: {
      $ref: "./db-models/RelCardConfigFieldConfig.json",
    },
  },
  {
    title: "DbModels",
  }
);
