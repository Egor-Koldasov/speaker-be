import { e2eSelector } from '../e2eSelector'

export const e2esToast = e2eSelector<{ text?: string }>(({ page, text = '' }) =>
  page.getByRole('status', { name: text }),
)
