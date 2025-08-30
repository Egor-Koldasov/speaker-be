import React, { createContext, useContext, useMemo } from 'react'
import { useColorScheme } from 'react-native'
import { darkColors, lightColors, ThemeColors } from './colors'
import { spacing } from './spacing'
import { font } from './typography'

export type Theme = ThemeColors & {
  spacing: typeof spacing
  font: typeof font
}

const ThemeContext = createContext<Theme | null>(null)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const colorScheme = useColorScheme()
  const theme = useMemo<Theme>(() => {
    const base = colorScheme === 'dark' ? darkColors : lightColors
    return { ...base, spacing, font }
  }, [colorScheme])

  return <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>
}

export function useTheme() {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider')
  return ctx
}
