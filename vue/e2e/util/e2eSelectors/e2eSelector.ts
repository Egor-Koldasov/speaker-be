import { Locator, Page } from '@playwright/test'
import { isType } from '../../../src/util/isType'

type E2eSelectorFn = (opts: { page: Page }) => Locator

export const e2eSelector = isType<E2eSelectorFn>
