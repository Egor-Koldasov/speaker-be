import { expect, test } from '@playwright/test'
import { testSignup } from './util/testActions/testSignup'
import { Tags } from './util/e2eSelectors/E2esTags'
import { clickWhenSingle } from './util/clickWhenSingle'

test('Definition builder', async ({ page }) => {
  await testSignup({ page })

  await test.step('Create a card config 1', async () => {
    await clickWhenSingle(Tags.Layout.pageNavigationButton({ page }))
    await Tags.PageNavigation.cardCreator({ page }).click()
    await Tags.CardCreator.createCardButton({ page }).click()
    await expect(Tags.Toast.cardCreated({ page })).toBeVisible()
    const selectedOption = await Tags.CardCreator.cardConfigSelector({
      page,
    }).evaluate(
      (sel: HTMLSelectElement) =>
        sel.options[sel.options.selectedIndex]?.textContent,
    )
    expect(selectedOption).toMatch(/^Unnamed card config 1$/)
  })

  const cardConfig1Name = `Test card config 1`

  await test.step('Rename card config 1', async () => {})

  await test.step('Create field config 1_1', async () => {})

  // await Tags.CardCreator.cardConfigSelector({ page }).selectOption({
  //   label: 'Unnamed card',
  // })
})
test.afterEach(async ({ page }) => {
  await page.pause()
})
