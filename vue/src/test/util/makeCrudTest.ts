import 'fake-indexeddb/auto'
import '../mocks/mockServiceWorker'
import { authorize } from '../../swClient/authorize'
import { getAuth } from '../../crdt/auth/auth'
import { uuidv7 } from '@kripod/uuidv7'
import { addUpdate } from '../../swClient/addUpdate'
import { actionMap } from '../../crdt/idb/actionMap'
import { mSchemaMap } from '../../crdt/idb/models/models'
import type { AllModelSchemas } from '../../../../struct/gen/models'
import { db } from './testDb'
import { expect, it } from 'vitest'
import { idbA } from '../../crdt/idb/idb'

export const makeCrudTest = <const Name extends keyof AllModelSchemas>(
  modelName: Name,
  createParams: () => Omit<AllModelSchemas[Name]['CreateParams'], 'Id' | 'UserId'>,
  updateParams: () => Omit<AllModelSchemas[Name]['UpdateParams'], 'Id'>,
  // createInput
) => {
  const actions = {
    Create: actionMap[`Create${modelName}`],
    Update: actionMap[`Update${modelName}`],
    Delete: actionMap[`Delete${modelName}`],
  }
  const crud = mSchemaMap[modelName].crud

  const testCreate = async () => {
    const mockEmail = `user1-${Date.now()}@test.com`
    await authorize({ Email: mockEmail })
    const auth = getAuth()
    if (!auth) throw new Error('auth is null')
    const id = uuidv7()

    await addUpdate(actions.Create.create({ ...createParams(), Id: id, UserId: auth.User.Id }))
    {
      const res = await db.selectFrom(crud.TableName).where('id', '=', id).selectAll().execute()
      expect(res).toHaveLength(1)
      const idbData = await (await idbA()).get(modelName, id)
      expect(idbData).not.toBeUndefined()
    }
    return { id }
  }
  const Create = async () => {
    it('Should CREATE', async () => {
      await testCreate()
    })
  }
  const Update = async () => {
    it('Should UPDATE', async () => {
      const { id } = await testCreate()
      const update = updateParams()
      await addUpdate(actions.Update.create({ ...update, Id: id }))

      const res = await db.selectFrom(crud.TableName).where('id', '=', id).selectAll().execute()
      expect(res).toHaveLength(1)
      const idbData = await (await idbA()).get(modelName, id)
      expect(idbData).not.toBeUndefined()
      Object.entries(update).forEach(([key, value]) => {
        expect((idbData as any)[key]).toEqual(value)
      })
    })
  }
  // const Delete = async () => {
  //   it('Should DELETE', async () => {
  //     const { id } = await testCreate()
  //     await addUpdate(actions.Delete.create({ Id: id }))
  //     const res = await db.selectFrom(crud.TableName).where('id', '=', id).selectAll().execute()
  //     expect(res[0]).toHaveProperty('deleted_at')
  //     const idbData = await (await idbA()).get(modelName, id)
  //     expect(idbData?.DeletedAt).toBeTruthy()
  //   })
  // }
  const Run = () => {
    void Create()
    void Update()
    // void Delete()
  }
  return { testCreate, Create, Update, Run }
}
