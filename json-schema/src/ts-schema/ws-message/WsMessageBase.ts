import { JSONSchema7, JSONSchema7TypeName } from "json-schema";
import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    name: {
      $ref: "./WsMessageName.json",
    },
    id: {
      type: "string",
    },
    responseForId: {
      type: "string",
    },
    data: {
      type: ["object"] as
        | ["object"]
        | JSONSchema7TypeName
        | JSONSchema7TypeName[]
        | undefined,
      properties: {} as JSONSchema7["properties"],
    },
    authToken: {
      type: ["string", "null"],
    },
    errors: {
      type: "array",
      items: {
        $ref: "../property/AppError.json" as string,
      },
    },
  },
  {
    title: "WsMessageBase",
    optional: ["responseForId"],
  }
);
