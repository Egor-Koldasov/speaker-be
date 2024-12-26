import '../../util/test/mockIndexedDb'
import { beforeEach, describe, test } from 'vitest'
import { WsService } from '../../planning/WsService'
import { useLensUser } from '@/planning/lense/useLensUser'
import { withSetup } from '../../util/test/withSetup'
import { idbInit } from '../../idb/idb'
import { withTimeout } from '../../util/withTimeout'

describe(`Lens User`, () => {
  beforeEach(() => {
    idbInit()
    WsService.init()
  })

  test(`should load the user`, async () => {
    const lensUser = withSetup(() => useLensUser())
    await withTimeout(() => {}, 1000)
  })
})
