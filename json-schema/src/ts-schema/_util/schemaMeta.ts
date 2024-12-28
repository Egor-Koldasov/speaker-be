import { MetaRelation } from "./MetaRelation";

export type SchemaMeta = {
  relation?: MetaRelation;
};

export const schemaMeta = (meta: SchemaMeta): SchemaMeta => meta;
