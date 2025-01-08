import { FieldConfigValueType } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { beforeAll, expect, test } from 'vitest'
import { idbInit } from '../../../idb/idb'
import { useCreateCardConfig } from '../../../planning/Action/useCreateCardConfig'
import { useCreateFieldConfig } from '../../../planning/Action/useCreateFieldConfig'
import { useLensQueryCardConfig } from '../../../planning/Lens/useLensQueryCardConfig'
import { useLensQueryUserCardConfigs } from '../../../planning/Lens/useLensQueryUserCardConfigs'
import { WsService } from '../../../planning/WsService'
import { makeDbModelBase } from '../../../util/model-factories/makeDbModelBase'
import { makeTestId } from '../../../util/test/makeTestId'
import { withSetup } from '../../../util/test/withSetup'
import { timeout } from '../../../util/timeout'
import { waitFor } from '../../../util/waitFor'
import { testSignup } from '../scenarios/signup'

beforeAll(() => {
  idbInit()
  WsService.init()
})
test('Create CardConfig', async () => {
  await testSignup()
  const {
    result: [
      actionCreateCardConfig,
      lensQueryUserCardConfigs,
      actionCreateFieldConfig,
    ],
  } = withSetup(() => [
    useCreateCardConfig(),
    useLensQueryUserCardConfigs(),
    useCreateFieldConfig(),
  ])
  actionCreateCardConfig.memActionParams.cardConfig = {
    ...makeDbModelBase({ name: 'CardConfig' }),
    name: `Test card config ${makeTestId()} ${new Date().toISOString()}`,
    prompt: 'Test prompt',
  }
  await timeout(0).promise
  actionCreateCardConfig.requestMainDb()
  expect(actionCreateCardConfig.waitingMainDbId).toBeTruthy()
  await waitFor(() => !actionCreateCardConfig.waitingMainDbId)
  lensQueryUserCardConfigs.requestMainDb()
  await waitFor(() => lensQueryUserCardConfigs.memData.cardConfigs.length === 1)
  expect(lensQueryUserCardConfigs.memData.cardConfigs[0]?.name).toBe(
    actionCreateCardConfig.memActionParams.cardConfig.name,
  )

  const {
    result: [lensQueryCardConfig],
  } = withSetup(() => [useLensQueryCardConfig()])

  const cardConfigId = actionCreateCardConfig.memActionParams.cardConfig.id

  lensQueryCardConfig.$state.memDataArgs = {
    cardConfigId,
  }
  await waitFor(() => {
    return lensQueryCardConfig.memData.cardConfig?.id === cardConfigId
  })
  actionCreateFieldConfig.$state.memActionParams.cardConfigId = cardConfigId
  actionCreateFieldConfig.$state.memActionParams.fieldConfig = {
    ...makeDbModelBase({ name: 'FieldConfig' }),
    name: `Test field config ${makeTestId()} ${new Date().toISOString()}`,
    prompt: 'Test prompt',
    valueType: FieldConfigValueType.Text,
    minResult: 1,
    maxResult: 3,
  }
  actionCreateFieldConfig.requestMainDb()
  expect(actionCreateFieldConfig.waitingMainDbId).toBeTruthy()
  await waitFor(() => !actionCreateFieldConfig.waitingMainDbId)

  await waitFor(() => {
    const fieldConfigByName =
      lensQueryCardConfig.memData.cardConfig?.fieldConfigByName ?? {}
    return Object.keys(fieldConfigByName).length === 1
  })
  const fieldConfig =
    lensQueryCardConfig.memData.cardConfig?.fieldConfigByName?.[
      actionCreateFieldConfig.$state.memActionParams.fieldConfig.id
    ]
  expect(
    fieldConfig?.name ===
      actionCreateFieldConfig.$state.memActionParams.fieldConfig.name,
  )
})
