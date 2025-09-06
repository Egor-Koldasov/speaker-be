export const normalizeLanguageCode = (languageCode: string) => {
  const locale = new Intl.Locale(languageCode)
  return locale.language
}
