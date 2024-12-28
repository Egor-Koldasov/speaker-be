import { moveRefs } from "../_util/moveRefs";
import { schemaObject } from "../_util/schemaObject";
import FieldValueSet from "../db-models/FieldValueSet";

export default schemaObject(
  {
    cardConfigId: {
      $ref: "../db-models/DbId.json",
    },
    fields: {
      type: "array",
      items: {
        ...moveRefs(FieldValueSet, "../db-models").properties,
        fieldValues: {
          type: "array",
          items: {
            $ref: "../db-models/FieldValue.json",
          },
        },
      },
    },
  },
  {
    title: "LensCardValue",
  }
);
