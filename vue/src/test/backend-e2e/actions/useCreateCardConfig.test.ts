import { beforeAll, describe, expect, test } from 'vitest'
import { testSignup } from '../scenarios/signup'
import { withSetup } from '../../../util/test/withSetup'
import { useCreateCardConfig } from '../../../planning/Action/useCreateCardConfig'
import { makeDbModelBase } from '../../../util/model-factories/makeDbModelBase'
import { makeTestId } from '../../../util/test/makeTestId'
import { waitFor } from '../../../util/waitFor'
import { idbInit } from '../../../idb/idb'
import { WsService } from '../../../planning/WsService'
import { useLensQueryUserCardConfigs } from '../../../planning/Lens/useLensQueryUserCardConfigs'
import { timeout } from '../../../util/timeout'

describe('useCreateCardConfig lensQueryUserCardConfigs', () => {
  beforeAll(() => {
    idbInit()
    WsService.init()
  })
  test('should create a card config', async () => {
    await testSignup()
    const {
      result: [actionCreateCardConfig, lensQueryUserCardConfigs],
    } = withSetup(() => [useCreateCardConfig(), useLensQueryUserCardConfigs()])
    actionCreateCardConfig.memActionParams.cardConfig = {
      ...makeDbModelBase(),
      name: `Test card config ${makeTestId()} ${new Date().toISOString()}`,
      // Ignored by design
      userId: '',
    }
    await timeout(0).promise
    actionCreateCardConfig.requestMainDb()
    expect(actionCreateCardConfig.waitingMainDbId).toBeTruthy()
    await waitFor(() => !actionCreateCardConfig.waitingMainDbId)
    lensQueryUserCardConfigs.requestMainDb()
    await waitFor(
      () => lensQueryUserCardConfigs.memData.cardConfigs.length === 1,
    )
    expect(lensQueryUserCardConfigs.memData.cardConfigs[0]?.name).toBe(
      actionCreateCardConfig.memActionParams.cardConfig.name,
    )

    // const {
    //   result: [actionCreateCardConfig, lensQueryUserCardConfigs],
    // } = withSetup(() => [useCreateCardConfig(), useLensQueryUserCardConfigs()])
  })
})
