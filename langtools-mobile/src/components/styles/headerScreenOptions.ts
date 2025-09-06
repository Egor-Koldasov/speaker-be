import { NativeStackNavigationOptions } from '@react-navigation/native-stack'
import { ColorTokens } from '../../theme/colors'

export const headerScreenOptions = (props: { colors: ColorTokens }) => {
  return {
    headerStyle: { backgroundColor: props.colors.surface },
    headerTitleStyle: { color: props.colors.textPrimary },
    headerTintColor: props.colors.accent,
  } satisfies NativeStackNavigationOptions
}
