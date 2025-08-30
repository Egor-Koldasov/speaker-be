import React from 'react'
import {
  TextInput as RNTextInput,
  TextInputProps as RNTextInputProps,
} from 'react-native'
import { useTheme } from '../../theme/index'
import { platformShadow } from '../../theme/shadows'

export type TextInputProps = RNTextInputProps & {
  error?: boolean
  fullWidth?: boolean
}

export function TextInput({
  error,
  fullWidth,
  style,
  ...rest
}: TextInputProps) {
  const { colors, spacing, font } = useTheme()

  return (
    <RNTextInput
      placeholderTextColor={colors.textMuted}
      {...rest}
      style={[
        {
          backgroundColor: colors.surface,
          color: colors.textPrimary,
          borderColor: error ? colors.danger : colors.border,
          borderWidth: 1,
          borderRadius: 12,
          paddingVertical: spacing.md,
          paddingHorizontal: spacing.lg,
          fontSize: font.size.md,
          width: fullWidth ? '100%' : undefined,
        },
        platformShadow('sm'),
        style,
      ]}
    />
  )
}
