import 'fake-indexeddb/auto'
import '../../mocks/mockServiceWorker'
import { describe, expect, it } from 'vitest'
import { db } from '../../util/testDb'
import { getAuth } from '../../../crdt/auth/auth'
import { authorize } from '../../../swClient/authorize'
import { timeout } from '../../../util/timeout'

describe('Authorize', () => {
  it('should work', async () => {
    const mockEmail = `user1-${Date.now()}@test.com`
    await authorize({ Email: mockEmail })
    {
      await timeout(100)
      const auth = getAuth()
      expect(auth).not.toBeNull()
      const res = await db.selectFrom('user').where('email', '=', mockEmail).selectAll().execute()
      expect(res).toHaveLength(1)
    }
  })
})
