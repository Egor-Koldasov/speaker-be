import test, { Page, expect } from '@playwright/test'
import { makeTestId } from '../../../util/test/makeTestId'
import { readTestEmailsTo } from '../../../util/test/readTestEmails'
import { E2esTags } from '../e2eSelectors/E2esTags'
import { clickWhenSingle } from '../clickWhenSingle'

export const testSignup = async (opts: { page: Page }) => {
  const { page } = opts
  await test.step('Sign up', async () => {
    const testEmail = `signup-test-${makeTestId()}-${Date.now()}@test.com`

    await test.step('Public Home', async () => {
      await page.goto('http://localhost:3001/')
      await expect(page.getByText('Welcome to early application')).toBeVisible()
    })
    await test.step('Authorize with email', async () => {
      await page.getByRole('link', { name: 'Login' }).click()
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
        expect(signUpCode).toHaveLength(6)
      }).toPass()
    })
    await test.step('Enter code', async () => {
      await page.getByLabel('Enter authentication code').click()
      await page.getByLabel('Enter authentication code').fill(signUpCode)
      await page.getByLabel('Enter authentication code').press('Enter')
    })
    await test.step('App home page', async () => {
      await clickWhenSingle(E2esTags.Layout.pageNavigationButton({ page }))
      await E2esTags.PageNavigation.settingsButton({ page }).click()
      await expect(page.getByText(testEmail)).toBeVisible()
      await clickWhenSingle(E2esTags.Layout.pageNavigationButton({ page }))
      await E2esTags.PageNavigation.appHomeButton({ page }).click()
    })
  })
}
