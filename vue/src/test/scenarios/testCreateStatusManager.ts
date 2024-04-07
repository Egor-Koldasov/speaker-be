import { expect } from 'vitest'
import { addUpdate } from '../../swClient/addUpdate'
import { actionMap } from '../../crdt/idb/actionMap'
import { uuidv7 } from '@kripod/uuidv7'
import { idbA } from '../../crdt/idb/idb'
import { authorize } from '../../swClient/authorize'
import { getAuth } from '../../crdt/auth/auth'
import { MSchemaStatusManager } from '../../crdt/idb/models/models'
import { db } from '../util/testDb'
import { testCreateNode } from './testCreateNode'

export const testCreateStatusManager = async () => {
  const { id: nodeId } = await testCreateNode()
  const mockEmail = `user1-${Date.now()}@test.com`
  await authorize({ Email: mockEmail })
  const auth = getAuth()
  if (!auth) throw new Error('auth is null')
  const id = uuidv7()
  await addUpdate(
    actionMap.CreateStatusManager.create({
      ...MSchemaStatusManager.default(undefined),
      Id: id,
      RootNodeId: nodeId,
      UserId: auth.User.Id,
    }),
  )
  {
    const res = await db.selectFrom('status_manager').where('id', '=', id).selectAll().execute()
    expect(res).toHaveLength(1)
    const idbData = await (await idbA()).get('StatusManager', id)
    expect(idbData).not.toBeUndefined()
  }
  return { id }
}
