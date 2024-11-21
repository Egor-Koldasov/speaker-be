import type { IDBPDatabase, IDBPTransaction, StoreNames } from 'idb'
import type { IdbSchema } from './idb'

export type Migration = (
  database: IDBPDatabase<IdbSchema>,
  oldVersion: number,
  newVersion: number | null,
  transaction: IDBPTransaction<
    IdbSchema,
    StoreNames<IdbSchema>[],
    'versionchange'
  >,
) => Promise<void>

export const idbMigrations: Migration[] = [
  async (db) => {
    db.createObjectStore('User', {
      keyPath: 'Id',
    })
    db.createObjectStore('UserSettings', {
      keyPath: 'Id',
    })
  },
  // async (db, oldVersion, newVersion, transaction) => {
  //   db.createObjectStore('Deck', {
  //     keyPath: 'Id',
  //   })
  //   const cardTypeStore = db.createObjectStore('CardType', {
  //     keyPath: 'Id',
  //   })
  //   cardTypeStore.createIndex('DeckId', 'DeckId', { multiEntry: true })
  //   const cardDataStore = db.createObjectStore('CardData', {
  //     keyPath: 'Id',
  //   })
  //   cardDataStore.createIndex('DeckId', 'DeckId', { multiEntry: true })
  //   cardDataStore.createIndex('CardTypeId', 'CardTypeId', { multiEntry: true })
  // },
]
