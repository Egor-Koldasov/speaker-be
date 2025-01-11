import { Locator, expect } from '@playwright/test'

export const clickWhenSingle = async (locator: Locator) => {
  await expect(locator).toHaveCount(1)
  await locator.click()
}
