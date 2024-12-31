import '../../../util/test/mockIndexedDb'
import { expect } from 'vitest'
import { useSignUpByEmail } from '../../../planning/Action/useSignUpByEmail'
import { useSignUpByEmailCode } from '../../../planning/Action/useSignUpByEmailCode'
import { useLensQueryUser } from '../../../planning/Lens/useLensQueryUser'
import { makeTestId } from '../../../util/test/makeTestId'
import { readTestEmailsTo } from '../../../util/test/readTestEmails'
import { withSetup } from '../../../util/test/withSetup'
import { waitFor } from '../../../util/waitFor'

export const testSignup = async () => {
  const [signUpAction] = withSetup(() => useSignUpByEmail())
  const [signUpByCodeAction] = withSetup(() => useSignUpByEmailCode())
  const [lensUser] = withSetup(() => useLensQueryUser())

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
    expect(signUpCode).toHaveLength(6)

    return true
  })
  signUpByCodeAction.memActionParams.code = signUpCode
  signUpByCodeAction.requestMainDb()
  expect(signUpByCodeAction.waitingMainDbId).toBeTruthy()
  await waitFor(() => !signUpByCodeAction.waitingMainDbId)
  await waitFor(() => !!signUpByCodeAction.lastResponse)
  expect(
    signUpByCodeAction.lastResponse?.data.actionParams.sessionToken,
  ).toHaveLength(12)

  await waitFor(() => !!lensUser.memData.user.email)
  await waitFor(() => lensUser.memData.user.email === testEmail)
}
