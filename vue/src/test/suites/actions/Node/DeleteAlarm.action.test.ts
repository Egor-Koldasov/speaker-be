import 'fake-indexeddb/auto'
import '../../../mocks/mockServiceWorker'
import { describe, expect, it } from 'vitest'
import { testCreateNodeAlarm } from '../../../scenarios/testCreateNodeAlarm'
import { db } from '../../../util/testDb'
import { idbA } from '../../../../crdt/idb/idb'
import { addUpdate } from '../../../../swClient/addUpdate'
import { actionMap } from '../../../../crdt/idb/actionMap'

describe('DeleteAlarm', () => {
  it('should work', async () => {
    const { alarmId } = await testCreateNodeAlarm()

    await addUpdate(actionMap.DeleteAlarm.create({ Id: alarmId }))

    const res = await db.selectFrom('alarm').where('id', '=', alarmId).selectAll().execute()
    expect(res).toHaveLength(0)
    const idbData = await (await idbA()).get('Alarm', alarmId)
    expect(idbData).toBeUndefined()
  })
})
