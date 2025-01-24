import { e2eSelector } from './e2eSelector'
import { e2esAppHomeButton } from './e2es/e2esAppHomeButton'
import { e2esCardCreatorButton } from './e2es/e2esCardCreatorButton'
import { e2esCreateCardButton } from './e2es/e2esCreateCardButton'
import { e2esPageNavigationButton } from './e2es/e2esPageNavigationButton'
import { e2esSettingsButton } from './e2es/e2esSettingsButton'
import { e2esToast } from './e2es/e2esToast'

export const E2esTags = {
  Layout: {
    pageNavigationButton: e2esPageNavigationButton,
  },
  PageNavigation: {
    settingsButton: e2esSettingsButton,
    appHomeButton: e2esAppHomeButton,
    cardCreator: e2esCardCreatorButton,
  },
  CardCreator: {
    createCardButton: e2esCreateCardButton,
    cardConfigSelector: e2eSelector(({ page }) =>
      page.getByLabel('Card config').and(page.locator('select')),
    ),
  },
  Toast: {
    toast: e2esToast,
    cardCreated: e2eSelector(({ page }) =>
      e2esToast({ page, text: 'Card config created ' }),
    ),
  },
}
export const Tags = E2esTags
