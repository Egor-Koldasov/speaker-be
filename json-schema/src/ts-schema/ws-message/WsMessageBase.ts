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
      type: "object",
    },
    errors: {
      type: "array",
      items: {
        $ref: "../property/AppError.json",
      },
    },
  },
  {
    title: "WsMessageBase",
    optional: ["responseForId"],
  }
);
