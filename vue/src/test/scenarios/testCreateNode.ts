import { expect } from 'vitest'
import { addUpdate } from '../../swClient/addUpdate'
import { actionMap } from '../../crdt/idb/actionMap'
import { uuidv7 } from '@kripod/uuidv7'
import { idbA } from '../../crdt/idb/idb'
import { authorize } from '../../swClient/authorize'
import { getAuth } from '../../crdt/auth/auth'
import { MSchemaNode } from '../../crdt/idb/models/models'
import { db } from '../util/testDb'

export const testCreateNode = async () => {
  const mockEmail = `user1-${Date.now()}@test.com`
  await authorize({ Email: mockEmail })
  const auth = getAuth()
  if (!auth) throw new Error('auth is null')
  const id = uuidv7()
  await addUpdate(
    actionMap.CreateNode.create({
      ...MSchemaNode.default(undefined),
      Id: id,
      UserId: auth.User.Id,
      ContentShort: 'Mock node 1',
    }),
  )
  {
    const res = await db.selectFrom('node').where('id', '=', id).selectAll().execute()
    expect(res).toHaveLength(1)
    const idbData = await (await idbA()).get('Node', id)
    expect(idbData).not.toBeUndefined()
  }
  return { id }
}
