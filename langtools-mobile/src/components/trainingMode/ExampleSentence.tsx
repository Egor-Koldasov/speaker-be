import { Pressable, StyleSheet } from 'react-native'
import { AiVocabularyAwareSentenceStream } from '../../../convex/utils/schema/aiVocabularyAwareSentenceSchema'
import { Theme, useTheme } from '../../theme'
import { Text } from '../ui/Text'
import { View } from '../ui/View'
import { useQuery } from 'convex/react'
import { api } from '../../../convex/_generated/api'
import { useMemo, useState } from 'react'
import { isNonNullable } from '../../utils/isNonNullable'

export type ExampleSentenceProps = {
  vocabularyAwareSentence:
    | NonNullable<AiVocabularyAwareSentenceStream['sentences']>[number]
    | undefined
    | null
}

export function ExampleSentence(props: ExampleSentenceProps) {
  const { vocabularyAwareSentence } = props
  const styles = getStyles(useTheme())
  const [selectedWord, setSelectedWord] = useState('')
  const wordInfoWords = useMemo(() => {
    const words = vocabularyAwareSentence?.wordsUsed || []
    return words.map((word) => word.headword).filter(isNonNullable)
  }, [vocabularyAwareSentence])
  const wordInfoResult = useQuery(api.vocabularyAwareSentence.getSentenceInfo, {
    words: wordInfoWords,
  })
  const wordToSentenceInfo = useMemo(() => {
    if (!wordInfoResult) return {}
    return Object.fromEntries(wordInfoResult.wordToSentenceInfoPairs)
  }, [wordInfoResult])

  const selectedWordInfo =
    wordToSentenceInfo[selectedWord] && wordToSentenceInfo[selectedWord][0]

  return (
    <View style={styles.sentenceBox}>
      <View style={styles.sentence}>
        {vocabularyAwareSentence?.wordsUsed?.map((wordUsed, index) => {
          const selected = wordUsed.headword === selectedWord
          return (
            <Pressable
              key={index}
              onPress={() =>
                setSelectedWord(!selected ? (wordUsed.headword ?? '') : '')
              }
              style={[selected && styles.wordPressableSelected]}
            >
              <Text
                style={[
                  styles.word,
                  wordUsed.headword &&
                    !wordToSentenceInfo[wordUsed.headword] &&
                    styles.wordNew,
                ]}
              >
                {wordUsed.sentenceForm}
              </Text>
            </Pressable>
          )
        })}
      </View>
      {selectedWordInfo && (
        <View style={styles.selectedWordBox}>
          <Text>{selectedWordInfo.dictionaryEntry?.headword}</Text>
          <Text>
            {selectedWordInfo.dictionaryEntrySenseTranslations[0]?.partOfSpeech}
          </Text>
          <Text>
            {selectedWordInfo.dictionaryEntrySenseTranslations[0]?.definition}
          </Text>
        </View>
      )}
    </View>
  )
}

const getStyles = (theme: Theme) =>
  StyleSheet.create({
    sentenceBox: {
      gap: 0,
      width: '100%',
    },
    sentence: {
      fontSize: theme.font.size.lg,
      gap: theme.spacing.xxs,
      flexDirection: 'row',
      flexWrap: 'wrap',
      justifyContent: 'center',
    },
    word: {
      fontSize: theme.font.size.lg,
    },
    wordNew: {
      color: theme.colors.accent,
    },
    wordPressableSelected: {
      backgroundColor: theme.colors.surface,
      borderBottomColor: theme.colors.accent,
      borderBottomWidth: 1,
    },
    selectedWordBox: {
      backgroundColor: theme.colors.surface,
      padding: theme.spacing.xs,
      borderRadius: theme.spacing.xs,
      gap: theme.spacing.xxs,
      // position: 'absolute',
      // top: '100%',
      // left: '0%',
      // transform: [{ translateX: '-100%' }],
      // zIndex: 1,
    },
  })
