import { MetaRelation } from "../_util/MetaRelation";
import { moveRefs } from "../_util/moveRefs";
import { schemaMeta } from "../_util/schemaMeta";
import { schemaObject } from "../_util/schemaObject";
import FieldConfig from "../db-models/FieldConfig";

export default schemaObject(
  {
    ...moveRefs(FieldConfig, "../db-models").properties,
    fieldConfigByName: {
      type: "object",
      additionalProperties: {
        $ref: "../db-models/FieldConfig.json",
      },
      description:
        "A map of nested fieldConfigs with their names as keys. Empty for leaf fieldConfigs.",
      meta: schemaMeta({
        relation: MetaRelation.ManyToMany,
      }),
    },
  },
  {
    title: "LensFieldConfig",
    description: "FieldConfig with its nested fieldConfigs loaded",
  }
);
