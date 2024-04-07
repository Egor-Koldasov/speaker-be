import { expect } from 'vitest'
import { addUpdate } from '../../swClient/addUpdate'
import { actionMap } from '../../crdt/idb/actionMap'
import { uuidv7 } from '@kripod/uuidv7'
import { db } from '../util/testDb'
import { TaskType } from '../../../../struct/gen/models'
import { dateStr } from '../../util/datetime/dateStr'
import { idbA } from '../../crdt/idb/idb'
import { authorize } from '../../swClient/authorize'
import { getAuth } from '../../crdt/auth/auth'

export const testCreateTask = async () => {
  const mockEmail = `user1-${Date.now()}@test.com`
  await authorize({ Email: mockEmail })
  const auth = getAuth()
  if (!auth) throw new Error('auth is null')
  const id = uuidv7()
  await addUpdate(
    actionMap.CreateTask.create({
      Id: id,
      UserId: auth.User.Id,
      Name: 'mock task',
      CategoryId: null,
      CreatedAt: dateStr(),
      Estimate: 0,
      Note: '',
      Status: '',
      Type: TaskType.Deadline,
    }),
  )
  console.log('indexedDB', indexedDB)
  {
    const res = await db.selectFrom('task').where('id', '=', id).selectAll().execute()
    expect(res).toHaveLength(1)
    const task = await (await idbA()).get('Task', id)
    expect(task).not.toBeUndefined()
  }
  return { id }
}
