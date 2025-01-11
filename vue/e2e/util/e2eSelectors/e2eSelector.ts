import { Locator, Page } from '@playwright/test'

type E2eSelectorFn<ExtraProps extends object> = (
  opts: { page: Page } & ExtraProps,
) => Locator

export const e2eSelector = <ExtraProps extends object>(
  fn: E2eSelectorFn<ExtraProps>,
) => fn
