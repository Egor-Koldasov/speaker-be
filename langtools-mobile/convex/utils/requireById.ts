import { Id, TableNames } from '../_generated/dataModel'
import { DatabaseReader } from '../_generated/server'

export const requireById = async <TableName extends TableNames>(
  db: DatabaseReader,
  id: Id<TableName>,
) => {
  const doc = await db.get(id)
  if (!doc) {
    throw new Error(`Document with id ${id} not found`)
  }
  return doc
}
