import { uuidv7 } from '@kripod/uuidv7'
import { chromium, type FullConfig } from '@playwright/test'

async function globalSetup(config: FullConfig) {
  const browser = await chromium.launch(config.projects[0].use)
  const page = await browser.newPage({ baseURL: config.projects[0].use.baseURL })
  const testEmail = `test_${uuidv7()}@test.com`
  await page.pause()

  await page.goto(`/autologin?email=${testEmail}`)
  await page.pause()
  await page.waitForFunction(
    ({ email }) => {
      return (window as any).sync?.auth?.User?.Email === email
    },
    { email: testEmail },
  )
  browser.close()
}

export default globalSetup
