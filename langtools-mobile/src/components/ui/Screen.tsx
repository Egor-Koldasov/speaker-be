import React from 'react'
import { SafeAreaView, ScrollView, ViewStyle } from 'react-native'
import { useTheme } from '../../theme/index'

export type ScreenProps = {
  children: React.ReactNode
  scroll?: boolean
  style?: ViewStyle | ViewStyle[]
}

export function Screen({ children, scroll, style }: ScreenProps) {
  const { colors } = useTheme()
  const content = scroll ? (
    <ScrollView contentContainerStyle={{ padding: 20 }}>{children}</ScrollView>
  ) : (
    children
  )
  return (
    <SafeAreaView
      style={[
        { flex: 1, backgroundColor: colors.background, padding: 20 },
        style,
      ]}
    >
      {content}
    </SafeAreaView>
  )
}
