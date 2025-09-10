export type ColorTokens = {
  background: string
  surface: string
  surfaceElevated: string
  primary: string
  primaryMuted: string
  accent: string
  textPrimary: string
  textSecondary: string
  textMuted: string
  border: string
  overlay: string
  success: string
  warning: string
  danger: string
  learning: string
}

export type ThemeColors = {
  dark: boolean
  colors: ColorTokens
}

// Night forest inspired, very dark green palette
export const darkColors: ThemeColors = {
  dark: true,
  colors: {
    background: '#0b1210',
    surface: '#0f1a17',
    surfaceElevated: '#14211d',
    primary: '#2aa574',
    primaryMuted: '#1f7d59',
    accent: '#3ddc97',
    textPrimary: '#e6f4ef',
    textSecondary: '#b7cfc7',
    textMuted: '#8aa29b',
    border: '#1d2a26',
    overlay: 'rgba(6,16,12,0.6)',
    success: '#3ddc97',
    warning: '#e3b341',
    danger: '#ec6d6a',
    learning: '#0b70d6',
  },
}

export const lightColors: ThemeColors = {
  dark: false,
  colors: {
    background: '#f7fbf9',
    surface: '#ecf5f1',
    surfaceElevated: '#e2efe9',
    primary: '#1b8a62',
    primaryMuted: '#156a4c',
    accent: '#1dbf73',
    textPrimary: '#0f1a17',
    textSecondary: '#23332d',
    textMuted: '#5e7a71',
    border: '#c9ddd6',
    overlay: 'rgba(0,0,0,0.06)',
    success: '#159f67',
    warning: '#be8d1e',
    danger: '#c45755',
    learning: '#2aa574',
  },
}
