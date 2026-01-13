import {
  toUIMessages,
  UIMessage,
  useThreadMessages,
} from '@convex-dev/agent/react'
import { useAction } from 'convex/react'
import { useLocalSearchParams } from 'expo-router'
import { useRef, useState } from 'react'
import { FlatList } from 'react-native'
import { api } from '../../../convex/_generated/api'
import { Button } from '../../components/ui/Button'
import { KeyboardAwareView } from '../../components/ui/KeyboardAwareView'
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
  const listRef = useRef<FlatList<UIMessage>>(null)
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

  const uiMessages = toUIMessages(messages.results)

  if (messages === undefined) return <Loading />

  return (
    <Screen style={{ padding: 0 }}>
      <KeyboardAwareView style={{ flex: 1 }}>
        <FlatList
          ref={listRef}
          style={{ flex: 1 }}
          contentContainerStyle={{ padding: 20, gap: spacing.md }}
          data={uiMessages}
          keyExtractor={(m) => m.id}
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

        <View
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
            children="Send"
            onPress={async () => {
              if (!threadId || !input.trim()) return
              const text = input.trim()
              setInput('')
              await sendMessage({ threadId, message: text })
            }}
          />
        </View>
      </KeyboardAwareView>
    </Screen>
  )
}

function MessageBubble({ message }: { message: UIMessage }) {
  const { colors, spacing } = useTheme()
  const isUser = message.role === 'user'
  const bg = isUser ? colors.primary : colors.surfaceElevated
  const textColor = colors.textPrimary
  const content = message.text
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
      <Text style={{ color: textColor }} selectable>
        {content}
      </Text>
    </View>
  )
}
