import 'fake-indexeddb/auto'
import '../../../mocks/mockServiceWorker'
import { describe, expect, it } from 'vitest'
import { addUpdate } from '../../../../swClient/addUpdate'
import { actionMap } from '../../../../crdt/idb/actionMap'
import { testCreateNode } from '../../../scenarios/testCreateNode'
import { idbA } from '../../../../crdt/idb/idb'
import { db } from '../../../util/testDb'

describe('UpdateNode', () => {
  it('should work', async () => {
    const { id } = await testCreateNode()
    const { id: id2 } = await testCreateNode()
    const { id: id3 } = await testCreateNode()
    await addUpdate(
      actionMap.UpdateNode.create({
        Id: id,
        ContentShort: 'Mock content 1 updated',
        ParentId: id2,
        RelFromIds: [id3],
      }),
    )
    {
      const res = await db.selectFrom('node').where('id', '=', id).selectAll().execute()
      expect(res).toHaveLength(1)
      expect(res[0].content_short).toBe('Mock content 1 updated')
      const idbData = await (await idbA()).get('Node', id)
      expect(idbData).not.toBeUndefined()
      expect(idbData?.ContentShort).toBe('Mock content 1 updated')
      expect(idbData?.ParentId).toBe(id2)
      expect(idbData?.RelFromIds).toEqual([id3])
    }
  })
  it('should work on RelFromIds only', async () => {
    const { id } = await testCreateNode()
    const { id: id3 } = await testCreateNode()
    await addUpdate(
      actionMap.UpdateNode.create({
        Id: id,
        RelFromIds: [id3],
      }),
    )
    {
      const res = await db
        .selectFrom('node_rel')
        .where('node_from_id', '=', id)
        .selectAll()
        .execute()
      expect(res).toHaveLength(1)
      expect(res[0].node_to_id).toBe(id3)
      const idbData = await (await idbA()).get('Node', id)
      expect(idbData).not.toBeUndefined()
      expect(idbData?.RelFromIds).toEqual([id3])
    }
  })
})
