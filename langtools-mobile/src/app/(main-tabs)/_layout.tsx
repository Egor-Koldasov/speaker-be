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
          ios: { backgroundColor: colors.surface },
          default: { backgroundColor: colors.surface },
        }),
        tabBarLabelStyle: { color: colors.textSecondary },
        tabBarActiveBackgroundColor: colors.surface,
      }}
    >
      <Tabs.Screen
        name="ai-chat/index"
        options={{
          title: 'AI Chat',
          tabBarIcon: ({ color, focused }) => (
            <Ionicons
              name={
                focused ? 'chatbubble-ellipses' : 'chatbubble-ellipses-outline'
              }
              color={color}
              size={24}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="generate-dictionary-entry"
        options={{
          title: 'Dictionary',
          tabBarIcon: ({ color, focused }) => (
            <Ionicons
              name={focused ? 'book' : 'book-outline'}
              color={color}
              size={24}
            />
          ),
        }}
      />
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
