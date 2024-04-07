import { expect } from 'vitest'
import dayjs from 'dayjs'
import { idb } from '../../crdt/idb/idb'
import { useByWeek } from '../../crdt/reactive/lenses/useByWeek'
import { waitForIdb } from '../util/waitForIdb'
import { addUpdate } from '../../swClient/addUpdate'

export const testTrackNew = async () => {
  const lensByWeek = useByWeek()
  await addUpdate({ name: 'trackNew', params: undefined })
  const timeEntries = await idb().getAll('TimeEntry')
  expect(timeEntries.length).toBe(1)
  const timeEntry = timeEntries[0]
  if (!timeEntry) return expect(timeEntry).toBeDefined()
  const timeEntryIdbCreateGetTime = dayjs().diff(timeEntry.start, 'millisecond')
  expect.soft(timeEntryIdbCreateGetTime).toBeLessThan(20)

  await waitForIdb()

  expect(lensByWeek.current[timeEntry.id]).toEqual(timeEntry)

  console.log('timeEntryIdbCreateGetTime', timeEntryIdbCreateGetTime)
}
