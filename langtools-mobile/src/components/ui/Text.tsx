import React from 'react'
import { Text as RNText, TextProps as RNTextProps } from 'react-native'
import { useTheme } from '../../theme/index'

export type TextProps = RNTextProps & {
  variant?: 'title' | 'subtitle' | 'body' | 'label'
  color?: 'primary' | 'secondary' | 'muted' | 'inverse'
}

export function Text({ variant = 'body', color, style, ...rest }: TextProps) {
  const { colors, font } = useTheme()

  const fontSize =
    variant === 'title'
      ? font.size.xl
      : variant === 'subtitle'
        ? font.size.lg
        : variant === 'label'
          ? font.size.sm
          : font.size.md

  const textColor =
    color === 'primary'
      ? colors.textPrimary
      : color === 'secondary'
        ? colors.textSecondary
        : color === 'muted'
          ? colors.textMuted
          : colors.textPrimary
  return (
    <RNText
      {...rest}
      style={[
        {
          color: textColor,
          fontSize,
          fontFamily: font.family.regular,
        },
        style,
      ]}
    />
  )
}
