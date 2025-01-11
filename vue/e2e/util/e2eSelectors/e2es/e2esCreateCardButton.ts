import { e2eSelector } from '../e2eSelector'

export const e2esCreateCardButton = e2eSelector(({ page }) =>
  page.getByRole('button', { name: '+' }),
)
