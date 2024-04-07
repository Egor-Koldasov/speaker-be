import { ModelTimeEntry, type TimeEntry } from '../crdt/idb/models/models'
import type { TimeEntryById } from '../crdt/reactive/lenses/useByWeek'

export const timeEntriesToMap = (timeEntries: TimeEntry[]) =>
  timeEntries.reduce<TimeEntryById>((acc, timeEntry) => {
    acc[timeEntry.id] = { ...ModelTimeEntry.default(undefined), ...timeEntry }
    return acc
  }, {})
