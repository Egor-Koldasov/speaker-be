import {
  ActionName,
  type User,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { idb } from '../../idb/idb'
import { LenseModelConfigMap } from '../LenseModelConfig'
import type { LenseModel } from '../LenseQuery'
import { defineUseLens } from '../DefineUseLens'

const initUser = {
  id: '',
  email: '',
  createdAt: '',
  updatedAt: '',
  deletedAt: null,
}
export const useLensUser = defineUseLens({
  name: 'User',
  initData: {
    user: initUser,
  },
  initParams: {},
  // async fetchIdb() {
  //   const [userIdb] = await (await idb()).getAll('User', undefined, 1)
  //   const user = !userIdb ? initUser : LenseModelConfigMap.User.fromIdb(userIdb)
  //   return { lensData: { user }, wantSync: false }
  // },
  async receiveMainDb(lensData) {
    const userIdb = LenseModelConfigMap.User.toIdb(lensData.user)
    await (await idb()).put('User', userIdb)
  },
  onActionResponse(message, store) {
    if (message.data.actionName === ActionName.SignUpByEmailCode) {
      store.refetch()
    }
  },
})
