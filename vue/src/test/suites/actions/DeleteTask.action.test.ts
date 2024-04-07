import 'fake-indexeddb/auto'
import '../../mocks/mockServiceWorker'
import { describe, expect, it } from 'vitest'
import { testCreateTask } from '../../scenarios/testCreateTask'
import { addUpdate } from '../../../swClient/addUpdate'
import { actionMap } from '../../../crdt/idb/actionMap'
import { db } from '../../util/testDb'
import { getAuth } from '../../../crdt/auth/auth'

describe('DeleteTask', () => {
  it('should work', async () => {
    const { id } = await testCreateTask()
    await addUpdate(
      actionMap.DeleteTask.create({
        Id: id,
      }),
    )
    {
      const res = await db.selectFrom('task').where('id', '=', id).selectAll().execute()
      const auth = getAuth()
      expect(res.filter((task) => task.user_id === auth?.User.Id)).toHaveLength(0)
    }
  })
})
