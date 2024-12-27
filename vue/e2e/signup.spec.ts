import { expect, test } from '@playwright/test'
import { makeTestId } from '../src/util/test/makeTestId'
import { readTestEmailsTo } from '../src/util/test/readTestEmails'

const viewportMobileDefault = { width: 375, height: 812 }
test.use({ viewport: viewportMobileDefault })

test('Signup', async ({ page }) => {
  const testEmail = `signup-test-${makeTestId()}-${Date.now()}@test.com`

  await test.step('Public Home', async () => {
    await page.goto('http://localhost:3001/')
    await expect(page.getByText('Welcome to early application')).toBeVisible()
  })
  await test.step('Authorize with email', async () => {
    await page.getByRole('button', { name: 'Authorize' }).click()
    await page.getByRole('textbox').click()
    await page.getByRole('textbox').fill(testEmail)
    await page.getByRole('textbox').press('Enter')
  })
  let signUpCode = ''
  await test.step('Check email code', async () => {
    expect(async () => {
      const emailsData = await readTestEmailsTo(testEmail)
      const email = emailsData.items[0]
      expect(email).toBeTruthy()

      signUpCode = email.Content.Body
      expect(signUpCode).toHaveLength(12)
    }).toPass()
  })
  await test.step('Enter code', async () => {
    await page.getByLabel('Enter authentication code').click()
    await page.getByLabel('Enter authentication code').fill(signUpCode)
    await page.getByLabel('Enter authentication code').press('Enter')
  })
  await test.step('App home page', async () => {
    await page.getByRole('button', { name: 'Settings' }).click()
    await expect(page.getByText(testEmail)).toBeVisible()
  })
})
test.afterEach(async ({ page }) => {
  await page.pause()
})
