import { defineStore, type StoreState } from 'pinia'
import { onMounted } from 'vue'
import { getLocalData, setLocalData } from '../util/localData'

const initState = {
  originalLanguages: [] as string[],
  translationLanguage: 'EN',
  primaryForeignLanguage: 'TH',
  nativeLanguages: [] as string[],
}
const useSettings_ = defineStore('uisSettings', {
  state: () => initState,
})

type Settings = StoreState<typeof initState>

export const useSettings = () => {
  const uisSettings = useSettings_()

  onMounted(() => {
    const settings = getLocalData<Settings>('uisSettings')
    if (settings) {
      Object.assign(uisSettings, settings)
      if (!settings.translationLanguage) {
        uisSettings.translationLanguage = 'EN'
      }
    }
  })

  uisSettings.$subscribe(() => {
    setLocalData('uisSettings', uisSettings.$state)
  })

  return uisSettings
}
