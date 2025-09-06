import Ionicons from '@expo/vector-icons/Ionicons'
import { useQuery } from 'convex/react'
import { useCallback, useMemo, useState } from 'react'
import { ScrollView, StyleSheet } from 'react-native'
import { api } from '../../../convex/_generated/api'
import { Button } from '../../components/ui/Button'
import { KeyboardAwareView } from '../../components/ui/KeyboardAwareView'
import { Screen } from '../../components/ui/Screen'
import { Text } from '../../components/ui/Text'
import { TextInput } from '../../components/ui/TextInput'
import { View } from '../../components/ui/View'
import { Theme, useTheme } from '../../theme'
import { useAction } from '../../utils/convex/useAction'
import { useMutation } from '../../utils/convex/useMutation'

const MOCK_DICTIONARY_ENTRY = {
  headword: 'run',
  sourceLanguage: 'English',
  senses: [
    {
      localId: '1',
      canonicalForm: 'run',
      definition:
        'To move swiftly on foot so that both feet leave the ground during each stride',
      partOfSpeech: 'verb',
    },
    {
      localId: '2',
      canonicalForm: 'run',
      definition: 'To operate or function',
      partOfSpeech: 'verb',
    },
    {
      localId: '3',
      canonicalForm: 'run',
      definition: 'A period of running as exercise or for pleasure',
      partOfSpeech: 'noun',
    },
    {
      localId: '4',
      canonicalForm: 'run',
      definition: 'A continuous series or sequence',
      partOfSpeech: 'noun',
    },
  ],
}

export default function GenerateDictionaryEntryPage() {
  const [inputText, setInputText] = useState('')
  const theme = useTheme()
  const [threadId, setThreadId] = useState('')
  const aiDictionaryEntryStream = useQuery(
    api.aiChat.getAiDictionaryEntryStream,
    !threadId ? 'skip' : { threadId },
  )

  const styles = useMemo(() => getStyles(theme), [theme])

  const generateDictionaryEntry = useAction(api.aiChat.generateDictionaryEntry)
  const createThread = useMutation(api.aiChat.createThread)

  const onGenerate = useCallback(async () => {
    if (!inputText.trim()) return
    const threadId = await createThread.mutate()
    setThreadId(threadId)
    await generateDictionaryEntry.exec({ headword: inputText, threadId })
  }, [createThread, generateDictionaryEntry, inputText])

  return (
    <Screen>
      <KeyboardAwareView style={styles.container}>
        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          <Text variant="title" style={styles.title}>
            Dictionary Entry
          </Text>

          <View
            background="surface"
            rounded="lg"
            padded
            style={styles.entryCard}
          >
            <Text variant="subtitle" style={styles.headword}>
              {aiDictionaryEntryStream?.headword}
            </Text>
            <Text variant="label" color="muted" style={styles.language}>
              {aiDictionaryEntryStream?.sourceLanguage}
            </Text>

            <View style={styles.sensesContainer}>
              {aiDictionaryEntryStream?.senses?.map((sense, index) => (
                <View key={sense.localId ?? index} style={styles.senseItem}>
                  <View style={styles.senseHeader}>
                    <Text variant="label" style={styles.senseNumber}>
                      {index + 1}.
                    </Text>
                    <Text
                      variant="label"
                      color="secondary"
                      style={styles.partOfSpeech}
                    >
                      {sense.partOfSpeech}
                    </Text>
                  </View>
                  <Text variant="body" style={styles.definition}>
                    {sense.definition}
                  </Text>
                </View>
              ))}
            </View>
          </View>
        </ScrollView>

        <View style={styles.inputContainer}>
          <TextInput
            placeholder="Enter a word to generate dictionary entry..."
            value={inputText}
            onChangeText={setInputText}
            fullWidth
            style={styles.textInput}
            returnKeyType="send"
            onSubmitEditing={onGenerate}
          />
          <Button
            title={<Ionicons name="send" size={16} color="white" />}
            onPress={onGenerate}
            style={styles.generateButton}
          />
        </View>
      </KeyboardAwareView>
    </Screen>
  )
}

const getStyles = (theme: Theme) =>
  StyleSheet.create({
    container: {
      flex: 1,
    },
    content: {
      flex: 1,
      paddingHorizontal: 16,
    },
    title: {
      marginBottom: 24,
      textAlign: 'center',
    },
    entryCard: {
      marginBottom: 24,
    },
    headword: {
      marginBottom: 4,
    },
    language: {
      marginBottom: 16,
    },
    sensesContainer: {
      gap: 16,
    },
    senseItem: {
      marginBottom: 12,
    },
    senseHeader: {
      flexDirection: 'row',
      alignItems: 'center',
      marginBottom: 4,
      gap: 8,
    },
    senseNumber: {
      fontWeight: '600',
      minWidth: 20,
    },
    partOfSpeech: {
      fontStyle: 'italic',
    },
    definition: {
      marginLeft: 28,
      lineHeight: 20,
    },
    inputContainer: {
      padding: theme.spacing.xs,
      gap: theme.spacing.xs,
      flexDirection: 'row',
    },
    textInput: {
      marginBottom: 0,
      flexShrink: 1,
    },
    generateButton: {
      alignSelf: 'stretch',
    },
  })
