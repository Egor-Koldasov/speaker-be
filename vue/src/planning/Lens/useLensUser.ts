import {
  LensQueryName,
  type User,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { defineUseLens } from '../DefineUseLens'

const initUser: User = {
  id: '',
  email: '',
  createdAt: '',
  updatedAt: '',
  deletedAt: null,
}
export const useLensUser = defineUseLens({
  name: LensQueryName.LensQueryUser,
  initData: {
    user: initUser,
  },
  initParams: {},
  // async fetchIdb() {
  //   const [userIdb] = await (await idb()).getAll('User', undefined, 1)
  //   const user = !userIdb ? initUser : LenseModelConfigMap.User.fromIdb(userIdb)
  //   return { lensData: { user }, wantSync: false }
  // },
  // async receiveMainDb(lensData) {
  //   const userIdb = LenseModelConfigMap.User.toIdb(lensData.user)
  //   await (await idb()).put('User', userIdb)
  // },
})
