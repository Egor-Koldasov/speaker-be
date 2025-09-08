import React from 'react'
import { ActivityIndicator, View } from 'react-native'
import { useTheme } from '../../theme/index'
import { Text } from './Text'

export type LoadingProps = {
  message?: string
  flex?: boolean
}

export function Loading({ message, flex = true }: LoadingProps) {
  const { colors, spacing } = useTheme()
  return (
    <View
      style={{
        flex: flex ? 1 : undefined,
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <ActivityIndicator size="large" color={colors.accent} />
      {message ? (
        <Text color="secondary" style={{ marginTop: spacing.md }}>
          {message}
        </Text>
      ) : null}
    </View>
  )
}
