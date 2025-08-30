import React from 'react'
import { Pressable, PressableProps, Text } from 'react-native'
import { useTheme } from '../../theme/index'
import { platformShadow } from '../../theme/shadows'

export type ButtonProps = PressableProps & {
  title: string
  tone?: 'primary' | 'secondary' | 'danger'
  size?: 'md' | 'lg'
  fullWidth?: boolean
}

export function Button({
  title,
  tone = 'primary',
  size = 'md',
  fullWidth,
  style,
  ...rest
}: ButtonProps) {
  const { colors, spacing, font } = useTheme()

  const bg =
    tone === 'danger'
      ? '#b84a48'
      : tone === 'secondary'
        ? colors.primaryMuted
        : colors.primary

  const paddingY = size === 'lg' ? spacing.lg : spacing.md
  const paddingX = spacing.xl
  const borderRadius = 14

  return (
    <Pressable
      accessibilityRole="button"
      {...rest}
      style={(state) => [
        {
          backgroundColor: state.pressed ? bg + 'cc' : bg,
          borderRadius,
          paddingVertical: paddingY,
          paddingHorizontal: paddingX,
          alignItems: 'center',
          justifyContent: 'center',
          width: fullWidth ? '100%' : undefined,
        },
        platformShadow('md'),
        typeof style === 'function' ? style(state) : style,
      ]}
    >
      <Text
        style={{
          color: colors.textPrimary,
          fontSize: size === 'lg' ? font.size.lg : font.size.md,
          fontWeight: '600',
        }}
      >
        {title}
      </Text>
    </Pressable>
  )
}
