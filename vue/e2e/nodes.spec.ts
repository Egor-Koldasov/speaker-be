import { expect, test } from '@playwright/test'
import { e2e } from './util/e2e'

test('Can create nodes', async ({ page }) => {
  await e2e.autoLogin(page)
  await page.getByRole('button', { name: '^' }).click()
  await page.getByLabel('Short content').click()
  await page.getByLabel('Short content').fill('First node')
  await page.keyboard.press('Meta+Enter')
  await expect(page.getByText('First node')).toBeVisible()
  await page.getByLabel('Short content').fill('Second node')
  await page.keyboard.press('Meta+Enter')
  await expect(page.getByText('Second node')).toBeVisible()

  await page.getByText('First node').click()
  await page.getByLabel('Short content').click()
  await page.getByLabel('Short content').fill('Third node')
  await page.keyboard.press('Meta+Enter')
  await expect(page.getByText('Third node')).toBeVisible()

  await page.getByRole('button', { name: '▼' }).click()
  await page.getByRole('button', { name: '▶' }).click()
  await page.getByRole('button', { name: '▼' }).press('Escape')
})
