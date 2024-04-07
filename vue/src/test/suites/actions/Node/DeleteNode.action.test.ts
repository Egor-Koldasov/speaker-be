import 'fake-indexeddb/auto'
import '../../../mocks/mockServiceWorker'
import { describe, expect, it } from 'vitest'
import { testCreateNode } from '../../../scenarios/testCreateNode'
import { idbA } from '../../../../crdt/idb/idb'
import { addUpdate } from '../../../../swClient/addUpdate'
import { actionMap } from '../../../../crdt/idb/actionMap'
import { db } from '../../../util/testDb'

describe('DeleteNode', () => {
  it('should work', async () => {
    const { id } = await testCreateNode()
    await addUpdate(
      actionMap.DeleteNode.create({
        Id: id,
      }),
    )
    {
      const res = await db.selectFrom('node').where('id', '=', id).selectAll().execute()
      expect(res).toHaveLength(0)
      const idbData = await (await idbA()).get('Node', id)
      expect(idbData).toBeUndefined()
    }
  })
})
