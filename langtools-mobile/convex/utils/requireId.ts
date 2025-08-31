import { TableNames } from '../_generated/dataModel'
import { DatabaseReader } from '../_generated/server'

export const requireId = <TableName extends TableNames>(
  db: DatabaseReader,
  tableName: TableName,
  id: string,
) => {
  const normalizedId = db.normalizeId(tableName, id)
  if (!normalizedId) {
    throw new Error(`Invalid ${tableName} ID: ${id}`)
  }
  return normalizedId
}
