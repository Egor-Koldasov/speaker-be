import { MetaRelation } from "../_util/MetaRelation";
import { schemaMeta } from "../_util/schemaMeta";
import { schemaObject } from "../_util/schemaObject";
import CardConfig from "../db-models/CardConfig";

export default schemaObject(
  {
    ...CardConfig.properties,
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
