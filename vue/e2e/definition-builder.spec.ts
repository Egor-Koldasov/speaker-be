import { test } from '@playwright/test'
import { testSignup } from './util/testActions/testSignup'

test('Definition builder', async ({ page }) => {
  await testSignup({ page })
})
test.afterEach(async ({ page }) => {
  await page.pause()
})
