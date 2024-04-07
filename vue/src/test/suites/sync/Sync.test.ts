import 'fake-indexeddb/auto'
import '../../mocks/mockServiceWorker'
import { beforeEach, describe, expect, it } from 'vitest'
import { testCreateTask } from '../../scenarios/testCreateTask'
import { db } from '../../util/testDb'
import { requestSync } from '../../../swClient/requestSync'
import { idbA } from '../../../crdt/idb/idb'
import { getAuth } from '../../../crdt/auth/auth'

describe('Sync', () => {
  beforeEach(() => {
    if (typeof window === 'object') window.indexedDB = new IDBFactory()
    if (typeof self === 'object') self.indexedDB = new IDBFactory()
  })
  it('should work', async () => {
    const { id } = await testCreateTask()

    {
      await (await idbA()).delete('Task', id)
      const idbTasks = await (await idbA()).getAll('Task')
      const auth = getAuth()
      expect(idbTasks.filter((task) => task.UserId === auth?.User.Id)).toHaveLength(0)
    }
    await requestSync()
    {
      const res = await db.selectFrom('task').where('id', '=', id).selectAll().execute()
      expect(res).not.toHaveLength(0)

      const idbTasks = await (await idbA()).getAll('Task')
      expect(idbTasks).not.toHaveLength(0)
    }
  })
})
