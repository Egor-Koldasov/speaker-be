import React from 'react'
import { ActivityIndicator, View } from 'react-native'
import { useTheme } from '../../theme/index'
import { Text } from './Text'

export type LoadingProps = {
  message?: string
}

export function Loading({ message }: LoadingProps) {
  const { colors, spacing } = useTheme()
  return (
    <View
      style={{
        flexShrink: 0,
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
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
