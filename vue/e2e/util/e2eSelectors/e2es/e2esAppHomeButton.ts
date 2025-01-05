import { e2eSelector } from '../e2eSelector'

export const e2esAppHomeButton = e2eSelector(({ page }) =>
  page.getByRole('link', { name: 'Home' }),
)
