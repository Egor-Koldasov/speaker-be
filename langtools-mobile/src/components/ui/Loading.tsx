import React from 'react'
import { ActivityIndicator, View } from 'react-native'
import { useTheme } from '../../theme/index'
import { Text } from './Text'

export type LoadingProps = {
  message?: string
  fullScreen?: boolean
}

export function Loading({ message = 'Loading…', fullScreen = true }: LoadingProps) {
  const { colors, spacing } = useTheme()
  return (
    <View
      style={{
        flex: fullScreen ? 1 : undefined,
        alignItems: 'center',
        justifyContent: 'center',
        padding: spacing.lg,
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


