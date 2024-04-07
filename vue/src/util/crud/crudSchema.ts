import { createCrud } from './createCrud'

export const crudSchema = {
  StatusManager: createCrud({ name: 'StatusManager', tableName: 'status_manager' }),
  Status: createCrud({ name: 'Status', tableName: 'status' }),
}
