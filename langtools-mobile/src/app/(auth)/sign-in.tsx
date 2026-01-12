import React from 'react'
import { SignIn as SignInForm } from '../../components/SignIn'
import { Screen } from '../../components/ui/Screen'
import { Text } from '../../components/ui/Text'
import { View } from '../../components/ui/View'
import { useTheme } from '../../theme/index'

export default function SignInScreen() {
  const { spacing } = useTheme()
  return (
    <Screen>
      <View style={{ gap: spacing.lg, padding: spacing.sm }}>
        <Text variant="title">Welcome</Text>
        <Text color="secondary">Sign in or create an account</Text>
        <View background="elevated" rounded="lg" padded>
          <SignInForm />
        </View>
      </View>
    </Screen>
  )
}
