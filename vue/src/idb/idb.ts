import { openDB, type DBSchema } from 'idb'
import type {
  LenseModelConfigMap,
  LenseModelIdbByName,
} from '../planning/LensModelConfig'
import { runPromiseSequence } from '../util/runPromiseSequence'
import { idbMigrations } from './idbMigrations'

export type IdbSchema = DBSchema & {
  User: {
    key: string
    value: LenseModelIdbByName<'User'>
  }
  UserSettings: {
    key: string
    value: LenseModelIdbByName<'UserSettings'>
  }
  // Deck: {
  //   key: string
  //   value: LenseModelIdbByName<'Deck'>
  // }
  // CardType: {
  //   key: string
  //   value: LenseModelIdbByName<'CardType'>
  //   indexes: {
  //     DeckId: string
  //   }
  // }
  // CardData: {
  //   key: string
  //   value: LenseModelIdbByName<'CardData'>
  //   indexes: {
  //     DeckId: string
  //     CardTypeId: string
  //   }
  // }
}

const version = 1

export const makeIdb = async () => {
  const db = await openDB<IdbSchema>('dataStore', version, {
    async upgrade(db, oldVersion, newVersion, transaction) {
      let dbVersion = oldVersion
      await runPromiseSequence(
        idbMigrations.map((migration, index) => {
          const versionI = index + 1
          if (versionI > dbVersion) {
            dbVersion = versionI
            console.log('IDB: applying migration', versionI)
            return () => migration(db, oldVersion, newVersion, transaction)
          }
          return () => Promise.resolve()
        }),
      )
    },
  })
  return db
}

let idbPromise: ReturnType<typeof makeIdb>

export const idbInit = () => {
  return
  // idbPromise = makeIdb()
  // window.idbPromise = idbPromise
}

export const idb = async () => {
  return idbPromise
}
