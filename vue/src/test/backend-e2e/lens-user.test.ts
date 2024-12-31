import '../../util/test/mockIndexedDb'
import { beforeEach, describe, test } from 'vitest'
import { WsService } from '../../planning/WsService'
import { useLensQueryUser } from '@/planning/Lens/useLensQueryUser'
import { withSetup } from '../../util/test/withSetup'
import { idbInit } from '../../idb/idb'
import { withTimeout } from '../../util/withTimeout'

describe(`Lens User`, () => {
  beforeEach(() => {
    idbInit()
    WsService.init()
  })

  test(`should load the user`, async () => {
    const lensUser = withSetup(() => useLensQueryUser())
    await withTimeout(() => {}, 1000)
  })
})
