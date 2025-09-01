import { useMutation, useQuery } from 'convex/react'
import { Link, useRouter } from 'expo-router'
import { FlatList, Pressable } from 'react-native'
import { api } from '../../../../convex/_generated/api'
import { Button } from '../../../components/ui/Button'
import { Loading } from '../../../components/ui/Loading'
import { Screen } from '../../../components/ui/Screen'
import { Text } from '../../../components/ui/Text'
import { View } from '../../../components/ui/View'
import { useTheme } from '../../../theme/index'

export default function AiChatThreads() {
  const { spacing } = useTheme()
  const router = useRouter()
  const threads = useQuery(api.aiChat.listThreads)
  const createThread = useMutation(api.aiChat.createThread)

  if (threads === undefined) return <Loading />

  return (
    <Screen>
      <View
        background="elevated"
        rounded="lg"
        padded
        style={{ gap: spacing.md }}
      >
        <Text variant="title">AI Chat</Text>
        <Text color="secondary">Your conversations</Text>
        <Button
          title="New Chat"
          size="lg"
          onPress={async () => {
            const threadId = await createThread({})
            router.push(`/ai-chat/${threadId}`)
          }}
        />
      </View>

      <FlatList
        contentContainerStyle={{
          paddingTop: spacing.lg,
          paddingBottom: 24,
          gap: spacing.md,
        }}
        data={threads}
        keyExtractor={(t) => t._id}
        renderItem={({ item }) => (
          <ThreadItem id={item._id} title={item.title} summary={item.summary} />
        )}
      />
    </Screen>
  )
}

function ThreadItem({
  id,
  title,
  summary,
}: {
  id: string
  title?: string
  summary?: string
}) {
  const { spacing } = useTheme()
  return (
    <Link href={`/ai-chat/${id}`} asChild>
      <Pressable>
        {({ pressed }) => (
          <View
            background="surface"
            rounded="lg"
            padded
            style={{ opacity: pressed ? 0.7 : 1, gap: spacing.xs }}
          >
            <Text variant="subtitle">{title ?? 'Untitled chat'}</Text>
            {!!summary && <Text color="muted">{summary}</Text>}
          </View>
        )}
      </Pressable>
    </Link>
  )
}
