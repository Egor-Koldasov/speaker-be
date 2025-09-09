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
import { apiToAiDictionaryEntry } from '../../utils/dictionary/apiToAiDictionaryEntry'
import { getSystemLanguageCode } from '../../utils/localization/getSystemLanguageCode'

export default function GenerateDictionaryEntryPage() {
  const [inputText, setInputText] = useState('')
  const theme = useTheme()
  const [threadId, setThreadId] = useState('')
  const aiDictionaryEntryStream = useQuery(
    api.aiChat.getAiDictionaryEntryStream,
    !threadId ? 'skip' : { threadId },
  )
  const dictionaryEntries = useQuery(
    api.dictionary.getDictionaryEntriesByHeadword,
    !inputText.trim() ? 'skip' : { headword: inputText },
  )

  const selectedDictionaryEntry = useMemo(() => {
    if (aiDictionaryEntryStream) return aiDictionaryEntryStream
    if (dictionaryEntries?.[0]) {
      return apiToAiDictionaryEntry(dictionaryEntries?.[0])
    }
    return null
  }, [aiDictionaryEntryStream, dictionaryEntries])

  const styles = useMemo(() => getStyles(theme), [theme])

  const generateDictionaryEntry = useAction(api.aiChat.generateDictionaryEntry)
  const createThread = useMutation(api.aiChat.createThread)

  const onGenerate = useCallback(async () => {
    if (!inputText.trim()) return
    const threadId = await createThread.mutate()
    setThreadId(threadId)
    await generateDictionaryEntry.exec({
      headword: inputText,
      threadId,
      translationLanguage: getSystemLanguageCode(),
    })
  }, [createThread, generateDictionaryEntry, inputText])

  return (
    <Screen>
      <KeyboardAwareView style={styles.container}>
        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {!!selectedDictionaryEntry && (
            <View
              background="surface"
              rounded="lg"
              padded
              style={styles.entryCard}
            >
              <Text variant="subtitle" style={styles.headword}>
                {selectedDictionaryEntry?.headword}
              </Text>
              <Text variant="label" color="muted" style={styles.language}>
                {selectedDictionaryEntry?.sourceLanguage}
              </Text>

              <View style={styles.sensesContainer}>
                {selectedDictionaryEntry?.senses?.map((sense, index) => (
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
          )}
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
          <Button onPress={onGenerate} style={styles.generateButton}>
            <Ionicons name="send" size={16} color="white" />
          </Button>
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
