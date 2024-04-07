import dayjs from 'dayjs'
import { testCreateNode } from './testCreateNode'
import { uuidv7 } from '@kripod/uuidv7'
import { actionMap } from '../../crdt/idb/actionMap'
import { addUpdate } from '../../swClient/addUpdate'
import { expect } from 'vitest'
import { idbA } from '../../crdt/idb/idb'
import { db } from '../util/testDb'

export const testCreateNodeAlarm = async () => {
  const { id } = await testCreateNode()
  const endDate = dayjs().add(1, 'day').toISOString()
  const alarmId = uuidv7()
  await addUpdate(
    actionMap.CreateNodeAlarm.create({
      NodeId: id,
      Id: alarmId,
      DateEnd: endDate,
    }),
  )
  {
    const res = await db.selectFrom('alarm').where('id', '=', alarmId).selectAll().execute()
    expect(res).toHaveLength(1)
    console.log('date_end', res[0].date_end, dayjs(res[0].date_end).toISOString())
    expect(dayjs(res[0].date_end).toISOString()).toBe(endDate)
    const idbData = await (await idbA()).get('Alarm', alarmId)
    expect(idbData).not.toBeUndefined()
    expect(idbData?.DateEnd).toBe(endDate)
  }
  return { id, alarmId }
}
