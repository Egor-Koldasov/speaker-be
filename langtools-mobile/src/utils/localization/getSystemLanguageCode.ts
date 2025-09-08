import { getLocales } from 'expo-localization'

export const getSystemLanguageCode = () => {
  const locale = getLocales()[0]
  if (!locale) {
    throw new Error('Unexpected: No locale found')
  }
  return locale.languageCode ?? 'en'
}
