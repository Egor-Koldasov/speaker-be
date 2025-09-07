import { useQuery } from 'convex/react'
import { useEffect, useMemo } from 'react'
import { StyleSheet } from 'react-native'
import { api } from '../../../convex/_generated/api'
import { Loading } from '../../components/ui/Loading'
import { Screen } from '../../components/ui/Screen'
import { Text } from '../../components/ui/Text'
import { View } from '../../components/ui/View'
import { Spacing, useTheme } from '../../theme'
import { useAction } from '../../utils/convex/useAction'

export default function TrainingMode() {
  const nextFsrsItems = useQuery(
    api.fsrsProgress.getNextFsrsItemWithTranslations,
    {
      limit: 1,
    },
  )
  const generateTranslations = useAction(
    api.dictionary.generateDictionaryEntryTranslation,
  )
  const isLoading = !nextFsrsItems
  const nextFsrsItem = nextFsrsItems?.[0]
  const theme = useTheme()
  const styles = useMemo(() => getStyles(theme), [theme])
  const translation = useMemo(
    () => nextFsrsItem?.senseTranslations[0],
    [nextFsrsItem],
  )
  const requireTranslations =
    !!nextFsrsItem && nextFsrsItem.senseTranslations.length === 0

  useEffect(() => {
    if (
      !nextFsrsItem ||
      !requireTranslations ||
      generateTranslations.isPending
    ) {
      return
    }
    generateTranslations.exec({
      dictionaryEntryId: nextFsrsItem.dictionaryEntry._id,
      translationLanguage: 'en',
    })
  }, [requireTranslations])

  return (
    <Screen>
      <View>
        {isLoading && <Loading />}
        {!nextFsrsItem && !isLoading && <Text>No items to review</Text>}
        {nextFsrsItem && (
          <View style={styles.questionBox}>
            <Text>{nextFsrsItem.dictionaryEntry.headword}</Text>
          </View>
        )}
        {generateTranslations.isPending && (
          <Text>Generating translations...</Text>
        )}
        {translation && (
          <View>
            <Text>{translation.partOfSpeech}</Text>
            <Text>{translation.canonicalForm}</Text>
            <Text>{translation.definition}</Text>
          </View>
        )}
      </View>
    </Screen>
  )
}

const getStyles = (theme: { spacing: Spacing }) =>
  StyleSheet.create({
    questionBox: {
      padding: theme.spacing.xs,
      alignItems: 'center',
    },
  })
