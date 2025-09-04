import { useThreadMessages } from '@convex-dev/agent/react'
import { useAction } from 'convex/react'
import { useLocalSearchParams } from 'expo-router'
import { useRef, useState } from 'react'
import {
  FlatList,
  KeyboardAvoidingView,
  Platform,
  View as RNView,
} from 'react-native'
import { api } from '../../../convex/_generated/api'
import { Button } from '../../components/ui/Button'
import { Loading } from '../../components/ui/Loading'
import { Screen } from '../../components/ui/Screen'
import { Text } from '../../components/ui/Text'
import { TextInput } from '../../components/ui/TextInput'
import { View } from '../../components/ui/View'
import { useTheme } from '../../theme/index'

export default function ThreadChat() {
  const { threadId } = useLocalSearchParams<{ threadId: string }>()
  const { spacing, colors } = useTheme()
  const [input, setInput] = useState('')
  const listRef = useRef<FlatList<any>>(null)
  const [isAtBottom, setIsAtBottom] = useState(true)

  const handleScroll = (e: any) => {
    const { contentOffset, layoutMeasurement, contentSize } = e.nativeEvent
    const threshold = 24
    const atBottom =
      contentOffset.y + layoutMeasurement.height >=
      contentSize.height - threshold
    setIsAtBottom(atBottom)
  }

  const messages = useThreadMessages(
    api.aiChat.listThreadMessages,
    { threadId },
    { initialNumItems: 100, stream: true },
  )
  const sendMessage = useAction(api.aiChat.sendRegularMessage)

  if (messages === undefined) return <Loading />

  return (
    <Screen style={{ padding: 0 }}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        keyboardVerticalOffset={88}
      >
        <FlatList
          ref={listRef}
          style={{ flex: 1 }}
          contentContainerStyle={{ padding: 20, gap: spacing.md }}
          data={messages.results}
          keyExtractor={(m) => m._id}
          renderItem={({ item }) => <MessageBubble message={item} />}
          onScroll={handleScroll}
          scrollEventThrottle={16}
          onContentSizeChange={() => {
            if (isAtBottom) {
              requestAnimationFrame(() => {
                listRef.current?.scrollToEnd({ animated: true })
              })
            }
          }}
        />

        <RNView
          style={{
            padding: 20,
            borderTopWidth: 1,
            borderTopColor: colors.border,
            gap: spacing.sm,
          }}
        >
          <TextInput
            placeholder="Type a message..."
            value={input}
            onChangeText={setInput}
            fullWidth
            multiline
          />
          <Button
            title="Send"
            onPress={async () => {
              if (!threadId || !input.trim()) return
              const text = input.trim()
              setInput('')
              await sendMessage({ threadId, message: text })
            }}
          />
        </RNView>
      </KeyboardAvoidingView>
    </Screen>
  )
}

function MessageBubble({ message }: { message: any }) {
  const { colors, spacing } = useTheme()
  const isUser = message.message?.role === 'user'
  const bg = isUser ? colors.primary : colors.surfaceElevated
  const textColor = colors.textPrimary
  const content =
    typeof message.message?.content === 'string'
      ? message.message?.content
      : Array.isArray(message.message?.content)
        ? message.message?.content.map((p: any) => p.text).join(' ')
        : (message.text ?? '')
  return (
    <View
      background={isUser ? undefined : 'elevated'}
      rounded="lg"
      padded
      style={{
        alignSelf: isUser ? 'flex-end' : 'flex-start',
        maxWidth: isUser ? '85%' : '100%',
        backgroundColor: bg,
        gap: spacing.xs,
      }}
    >
      <Text style={{ color: textColor }}>{content}</Text>
    </View>
  )
}
