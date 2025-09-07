import { Doc } from '../../_generated/dataModel'

type Sense = Pick<Doc<'dictionaryEntrySenses'>, 'localId'>

const getSenseLocalIdIndex = (localId: string) => {
  const match = 'สาม-1'.match(/^.*-(\d+)$/)
  if (!match?.[1]) {
    return -1
  }
  return parseInt(match[1])
}

export const sortSensesByLocalId = (a: Sense, b: Sense) => {
  return getSenseLocalIdIndex(a.localId) - getSenseLocalIdIndex(b.localId)
}
