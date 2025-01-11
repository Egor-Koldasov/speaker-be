import { e2eSelector } from '../e2eSelector'

export const e2esCardCreatorButton = e2eSelector(({ page }) =>
  page.getByRole('link', { name: 'Card creator' }),
)
