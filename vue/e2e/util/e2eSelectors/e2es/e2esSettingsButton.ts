import { e2eSelector } from '../e2eSelector'

export const e2esSettingsButton = e2eSelector(({ page }) =>
  page.getByRole('link', { name: 'Settings' }),
)
