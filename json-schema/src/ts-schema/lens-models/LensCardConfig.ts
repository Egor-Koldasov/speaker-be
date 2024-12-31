import { MetaRelation } from "../_util/MetaRelation";
import { moveRefs } from "../_util/moveRefs";
import { schemaMeta } from "../_util/schemaMeta";
import { schemaObject } from "../_util/schemaObject";
import CardConfig from "../db-models/CardConfig";

export default schemaObject(
  {
    ...moveRefs(CardConfig, "../db-models").properties,
    fieldConfigs: {
      type: "array",
      items: {
        $ref: "../db-models/FieldConfig.json",
      },
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
