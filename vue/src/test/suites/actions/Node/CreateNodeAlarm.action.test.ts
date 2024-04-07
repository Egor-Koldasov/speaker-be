import 'fake-indexeddb/auto'
import '../../../mocks/mockServiceWorker'
import { describe, it } from 'vitest'
import { testCreateNodeAlarm } from '../../../scenarios/testCreateNodeAlarm'

describe('CreateNodeAlarm', () => {
  it('should work', async () => {
    await testCreateNodeAlarm()
  })
})
