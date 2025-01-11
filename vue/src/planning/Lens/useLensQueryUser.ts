import { LensQueryName, type User } from 'speaker-json-schema'
import { defineUseLensQuery } from '../DefineUseLens'

const initUser: User = {
  id: '',
  email: '',
  createdAt: '',
  updatedAt: '',
  deletedAt: null,
}
export const useLensQueryUser = defineUseLensQuery({
  name: LensQueryName.User,
  initData: {
    user: initUser,
  },
  initMemDataArgs: {},
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
