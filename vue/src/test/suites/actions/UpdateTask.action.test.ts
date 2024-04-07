import 'fake-indexeddb/auto'
import '../../mocks/mockServiceWorker'
import { describe, expect, it } from 'vitest'
import { testCreateTask } from '../../scenarios/testCreateTask'
import { addUpdate } from '../../../swClient/addUpdate'
import { actionMap } from '../../../crdt/idb/actionMap'
import { db } from '../../util/testDb'

describe('UpdateTask', () => {
  it('should work', async () => {
    const { id } = await testCreateTask()
    await addUpdate(
      actionMap.UpdateTask.create({
        Id: id,
        Name: 'mock task updated',
      }),
    )
    {
      const res = await db.selectFrom('task').where('id', '=', id).selectAll().execute()
      expect(res).toHaveLength(1)
      expect(res[0].name).toBe('mock task updated')
    }
  })
})
