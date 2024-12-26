import { beforeAll, describe, expect, test } from 'vitest'
import { withSetup } from '../../../util/test/withSetup'
import { useSignUpByEmail } from '../../../planning/Action/useSignUpByEmail'
import { waitFor } from '../../../util/waitFor'
import { WsService } from '../../../planning/WsService'
import { readTestEmailsTo } from '../../../util/test/readTestEmails'
import { makeTestId } from '../../../util/test/makeTestId'

describe(`Signup`, () => {
  beforeAll(() => {
    WsService.init()
  })
  test(`Can signup`, async () => {
    const [signUpAction] = withSetup(() => useSignUpByEmail())

    const testEmail = `signup-test-${makeTestId()}@test.com`

    signUpAction.memActionParams.email = testEmail
    signUpAction.requestMainDb()
    expect(signUpAction.waitingMainDbId).toBeTruthy()
    await waitFor(() => !signUpAction.waitingMainDbId)
    let signUpCode = ''
    await waitFor(async () => {
      const emailsData = await readTestEmailsTo(testEmail)
      const email = emailsData.items[0]
      if (emailsData.count !== 1 || !email) return false

      signUpCode = email.Content.Body
      expect(signUpCode).toHaveLength(12)

      return true
    })
    // expect(signUpAction.waitingMainDbId).toBeTruthy()
  })
})
