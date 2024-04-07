import 'fake-indexeddb/auto'
import '../../../mocks/mockServiceWorker'
import { describe, it } from 'vitest'
import { testCreateNode } from '../../../scenarios/testCreateNode'

describe('CreateNode', () => {
  it('should work', async () => {
    await testCreateNode()
  })
})
