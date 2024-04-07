import 'fake-indexeddb/auto'
import '../../mocks/mockServiceWorker'
import { describe, it } from 'vitest'
import { testCreateTask } from '../../scenarios/testCreateTask'

describe('CreateTask', () => {
  it('should work', async () => {
    await testCreateTask()
  })
})
