import { beforeAll, describe, test } from 'vitest'
import { idbInit } from '../../../idb/idb'
import { WsService } from '../../../planning/WsService'
import { testSignup } from '../scenarios/signup'

describe(`Signup`, () => {
  beforeAll(() => {
    idbInit()
    WsService.init()
  })
  test(`Can signup`, async () => {
    await testSignup()
  })
})
