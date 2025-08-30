import React from 'react'
import { View as RNView, ViewProps as RNViewProps } from 'react-native'
import { useTheme } from '../../theme/index'

export type ViewProps = RNViewProps & {
  background?: 'background' | 'surface' | 'elevated'
  rounded?: 'sm' | 'md' | 'lg' | 'xl'
  padded?: boolean
}

export function View({
  background,
  rounded,
  padded,
  style,
  ...rest
}: ViewProps) {
  const { colors, spacing } = useTheme()
  const bgColor =
    background === 'surface'
      ? colors.surface
      : background === 'elevated'
        ? colors.surfaceElevated
        : undefined
  const radius =
    rounded === 'sm'
      ? 8
      : rounded === 'md'
        ? 12
        : rounded === 'lg'
          ? 16
          : rounded === 'xl'
            ? 24
            : 0

  return (
    <RNView
      {...rest}
      style={[
        {
          backgroundColor: bgColor ?? undefined,
          borderRadius: radius,
          padding: padded ? spacing.md : undefined,
        },
        style,
      ]}
    />
  )
}
