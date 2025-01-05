import { e2eSelector } from '../e2eSelector'

export const e2esPageNavigationButton = e2eSelector(({ page }) =>
  page.getByRole('button', { name: 'Page Navigation' }),
)
