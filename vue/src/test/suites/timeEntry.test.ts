import 'fake-indexeddb/auto'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, it } from 'vitest'
import { testTrackNew } from '../scenarios/testTrackNew'

describe.todo(`TimeEntry`, () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })
  it('Should cover basics', async () => {
    await testTrackNew()
  })
})
