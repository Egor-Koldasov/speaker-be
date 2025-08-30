export const font = {
  family: {
    regular: 'System',
    mono: 'SpaceMono',
  },
  size: {
    xs: 12,
    sm: 14,
    md: 16,
    lg: 20,
    xl: 24,
    xxl: 32,
  },
  lineHeight: {
    tight: 1.2,
    normal: 1.4,
    relaxed: 1.6,
  },
} as const

export type FontSizeKey = keyof typeof font.size


