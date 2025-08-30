import Ionicons from '@expo/vector-icons/Ionicons'
import { Tabs } from 'expo-router'
import { Platform } from 'react-native'
import { useTheme } from '../../theme/index'

export default function MainTabsLayout() {
  const { colors } = useTheme()
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: colors.accent,
        tabBarInactiveTintColor: colors.textMuted,
        tabBarStyle: Platform.select({
          ios: { position: 'absolute', backgroundColor: colors.surface },
          default: { backgroundColor: colors.surface },
        }),
        tabBarLabelStyle: { color: colors.textSecondary },
        tabBarActiveBackgroundColor: colors.surface,
      }}
    >
      <Tabs.Screen
        name="user-profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, focused }) => (
            <Ionicons
              name={focused ? 'person-circle-sharp' : 'person-circle-outline'}
              color={color}
              size={24}
            />
          ),
        }}
      />
    </Tabs>
  )
}
