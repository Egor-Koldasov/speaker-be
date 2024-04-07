import 'fake-indexeddb/auto'
import '../../mocks/mockServiceWorker'
import { describe, expect, it } from 'vitest'
import { addUpdate } from '../../../swClient/addUpdate'
import { actionMap } from '../../../crdt/idb/actionMap'
import { uuidv7 } from '@kripod/uuidv7'
import { db } from '../../util/testDb'
import { dateStr } from '../../../util/datetime/dateStr'
import { authorize } from '../../../swClient/authorize'
import { getAuth } from '../../../crdt/auth/auth'

describe('createCategory', () => {
  it('should work', async () => {
    const mockEmail = `user1-${Date.now()}@test.com`
    await authorize({ Email: mockEmail })
    const auth = getAuth()
    if (!auth) throw new Error('auth is null')

    const id = uuidv7()
    await addUpdate(
      actionMap.UpsertCategory.create({
        Id: id,
        Name: 'mock category',
        Color: '#000000',
        CreatedAt: dateStr(),
        UserId: auth.User.Id,
      }),
    )
    {
      const res = await db.selectFrom('category').where('id', '=', id).selectAll().execute()
      expect(res).toHaveLength(1)
      expect(res[0].user_id).toBe(auth?.User.Id)
    }

    await addUpdate(
      actionMap.UpsertCategory.create({
        UserId: auth.User.Id,
        Id: id,
        Name: 'mock category updated',
        Color: '#000000',
        CreatedAt: dateStr(),
      }),
    )

    const res = await db.selectFrom('category').where('id', '=', id).selectAll().execute()
    expect(res).toHaveLength(1)
    expect(res[0].name).toBe('mock category updated')
  })
})
