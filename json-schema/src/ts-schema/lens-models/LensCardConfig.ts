import { MetaRelation } from "../_util/MetaRelation";
import { moveRefs } from "../_util/moveRefs";
import { schemaMeta } from "../_util/schemaMeta";
import { schemaObject } from "../_util/schemaObject";
import CardConfig from "../db-models/CardConfig";

export default schemaObject(
  {
    ...moveRefs(CardConfig, "../db-models").properties,
    fieldConfigByName: {
      type: "object",
      additionalProperties: {
        $ref: "../db-models/FieldConfig.json",
      },
      description: "A map of fieldConfigs with their names as keys",
      meta: schemaMeta({
        relation: MetaRelation.ManyToMany,
      }),
    },
  },
  {
    title: "LensCardConfig",
    description: "CardConfig with its fieldConfigs loaded",
  }
);
