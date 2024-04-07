import { idbA, type IdbSchema } from '../../crdt/idb/idb'
import type { AllModelSchemas } from '../../../../struct/gen/models'
import { dateStr } from '../datetime/dateStr'

export type ModelBase = {
  Id: string
  CreatedAt: string
  UpdatedAt: string
  DeletedAt: string | null
}
export type UpdateBase = Partial<Omit<ModelBase, 'CreatedAt'>> & {
  Id: string
}
export type DeleteBase = {
  Id: string
}

export type Crud<Name extends keyof AllModelSchemas> = {
  Create: (model: AllModelSchemas[Name]['CreateParams']) => Promise<void>
  Update: (update: AllModelSchemas[Name]['UpdateParams']) => Promise<void>
  Delete: (params: DeleteBase) => Promise<void>
  GetAll: () => Promise<IdbSchema[Name]['value'][]>
  Name: Name
  TableName: AllModelSchemas[Name]['TableName']
}

export type CrudOptions<Name extends keyof AllModelSchemas> = {
  name: Name
  tableName: AllModelSchemas[Name]['TableName']
}

export const createCrud = <const Name extends keyof AllModelSchemas>(
  opts: CrudOptions<Name>,
): Crud<Name> => {
  const crudI: Crud<Name> = {
    Create: async (model) => {
      const idb = await idbA()
      await idb.put(opts.name, model as any)
    },
    Update: async (update) => {
      const idb = await idbA()
      const prevModel = await idb.get(opts.name, update.Id)
      if (!prevModel) throw new Error(`${opts.name} not found ${update.Id}`)
      const nextModel = { ...prevModel, ...update }
      await idb.put(opts.name, nextModel)
    },
    Delete(params: DeleteBase) {
      return crudI.Update({ Id: params.Id, DeletedAt: dateStr() })
    },
    async GetAll() {
      const idb = await idbA()
      const models = await idb.getAll(opts.name)
      return models as IdbSchema[Name]['value'][]
    },
    Name: opts.name,
    TableName: opts.tableName,
  }
  return crudI
}
