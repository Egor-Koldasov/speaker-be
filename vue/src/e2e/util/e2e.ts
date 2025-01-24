import { uuidv7 } from '@kripod/uuidv7'
import { Page } from '@playwright/test'

export const e2e = {
  autoLogin: async (page: Page) => {
    const testEmail = `test_${uuidv7()}@test.com`

    await page.goto(`/autologin?email=${testEmail}`)
    await page.waitForFunction(
      ({ email }) => {
        return (window as any).sync?.auth?.User?.Email === email
      },
      { email: testEmail },
    )
  },
}
