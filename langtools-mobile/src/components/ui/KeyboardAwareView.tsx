import {
  KeyboardAvoidingView,
  Platform,
  StyleProp,
  ViewStyle,
} from 'react-native'

export type KeyboardAwareViewProps = {
  children: React.ReactNode
  behavior?: 'padding' | 'height'
  keyboardVerticalOffset?: number
  style?: StyleProp<ViewStyle>
}

export function KeyboardAwareView({
  children,
  behavior,
  keyboardVerticalOffset = 88,
  style,
}: KeyboardAwareViewProps) {
  if (behavior === undefined) {
    behavior = Platform.OS === 'ios' ? 'padding' : undefined
  }
  return (
    <KeyboardAvoidingView
      behavior={behavior}
      keyboardVerticalOffset={keyboardVerticalOffset}
      style={[
        {
          flex: 1,
        },
        style,
      ]}
    >
      {children}
    </KeyboardAvoidingView>
  )
}
