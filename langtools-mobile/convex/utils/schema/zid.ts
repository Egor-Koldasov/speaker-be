import { zid as zid_ } from 'convex-helpers/server/zod'
import { TableNames } from '../../_generated/dataModel'

export const zid = <TableName extends TableNames>(tableName: TableName) =>
  zid_(tableName)
