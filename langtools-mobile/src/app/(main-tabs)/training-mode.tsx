import { useQuery } from 'convex/react'
import { StatusBar } from 'expo-status-bar'
import { useCallback, useEffect, useMemo } from 'react'
import { StyleSheet } from 'react-native'
import { proxy, useSnapshot } from 'valtio'
import { api } from '../../../convex/_generated/api'
import { Id } from '../../../convex/_generated/dataModel'
import { TrainingModeHeader } from '../../components/trainingMode/TrainingModeHeader'
import { Button } from '../../components/ui/Button'
import { Loading } from '../../components/ui/Loading'
import { Screen } from '../../components/ui/Screen'
import { Text } from '../../components/ui/Text'
import { View } from '../../components/ui/View'
import { Font, Spacing, useTheme } from '../../theme'
import { useAction } from '../../utils/convex/useAction'
import { withRetry } from '../../utils/convex/withRetry'
import { getSystemLanguageCode } from '../../utils/localization/getSystemLanguageCode'

enum QuestionStage {
  Question = 'question',
  Answer = 'answer',
}

const trainingState = proxy({
  questionStage: QuestionStage.Question,
  generateTranslationAttempt: 0,
})

export default function TrainingMode() {
  const snap = useSnapshot(trainingState)
  const nextFsrsItems = useQuery(
    api.fsrsProgress.getNextFsrsItemWithTranslations,
    {
      limit: 1,
    },
  )
  const generateTranslations = useAction(
    api.dictionary.generateDictionaryEntryTranslation,
  )
  const processReview = useAction(api.fsrsProgress.processReview)
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

  const generateTranslationsWithRetry = useCallback(
    async (dictionaryEntryId: Id<'dictionaryEntries'>) => {
      trainingState.generateTranslationAttempt = 0
      await withRetry({
        fn: () =>
          generateTranslations.exec({
            dictionaryEntryId,
            translationLanguage: getSystemLanguageCode(),
          }),
        onRetry: (error, attempt) => {
          trainingState.generateTranslationAttempt = attempt + 1
        },
      })
    },
    [generateTranslations],
  )

  useEffect(() => {
    if (
      !nextFsrsItem ||
      !requireTranslations ||
      generateTranslations.isPending
    ) {
      return
    }
    generateTranslationsWithRetry(nextFsrsItem.dictionaryEntry._id)
  }, [requireTranslations])

  return (
    <Screen>
      <View style={styles.trainingContainer}>
        <StatusBar animated={true} backgroundColor="#ffb507" />
        <TrainingModeHeader />
        <View style={styles.mainContent}>
          {isLoading && <Loading />}
          {!nextFsrsItem && !isLoading && <Text>No items to review</Text>}
          {nextFsrsItem && (
            <View style={styles.questionBox}>
              <Text style={styles.headword} selectable>
                {nextFsrsItem.dictionaryEntry.headword}
              </Text>
            </View>
          )}
          {snap.questionStage === QuestionStage.Answer && (
            <>
              <View style={styles.answerBox}>
                {generateTranslations.isPending && (
                  <Loading
                    message={`Generating translations. ${snap.generateTranslationAttempt > 0 && ` Retry attempt ${snap.generateTranslationAttempt + 1}`}.`}
                  />
                )}
                {translation && (
                  <>
                    <Text selectable>{translation.partOfSpeech}</Text>
                    <Text selectable>{translation.canonicalForm}</Text>
                    <Text selectable>
                      {translation.translations.join(', ')}
                    </Text>
                    <Text selectable selectionColor={theme.colors.accent}>
                      {translation.definition}
                    </Text>
                  </>
                )}
              </View>
            </>
          )}
        </View>
        {nextFsrsItem && (
          <View style={styles.buttonContainer}>
            {processReview.isPending && <Loading />}
            {!processReview.isPending && (
              <>
                {snap.questionStage === QuestionStage.Question && (
                  <Button
                    fullWidth
                    onPress={() =>
                      (trainingState.questionStage = QuestionStage.Answer)
                    }
                  >
                    Show Answer
                  </Button>
                )}
                {snap.questionStage === QuestionStage.Answer && (
                  <>
                    <Button
                      fullWidth
                      tone="danger"
                      onPress={async () => {
                        await processReview.exec({
                          fsrsProgressId: nextFsrsItem.fsrsProgress._id,
                          rating: 1,
                        })
                        trainingState.questionStage = QuestionStage.Question
                      }}
                    >
                      Forgot
                    </Button>
                    <Button
                      fullWidth
                      onPress={async () => {
                        await processReview.exec({
                          fsrsProgressId: nextFsrsItem.fsrsProgress._id,
                          rating: 3,
                        })
                        trainingState.questionStage = QuestionStage.Question
                      }}
                    >
                      Remember
                    </Button>
                  </>
                )}
              </>
            )}
          </View>
        )}
      </View>
    </Screen>
  )
}

const getStyles = (theme: { spacing: Spacing; font: Font }) =>
  StyleSheet.create({
    trainingContainer: {
      flex: 1,
    },
    mainContent: {
      flex: 1,
      flexGrow: 1,
    },
    questionBox: {
      padding: theme.spacing.sm,
      alignItems: 'center',
    },
    headword: {
      fontSize: theme.font.size.xl,
      paddingVertical: theme.spacing.xs,
    },
    answerBox: {
      padding: theme.spacing.sm,
    },
    buttonContainer: {
      padding: theme.spacing.xs,
      flexDirection: 'row',
      gap: theme.spacing.xs,
    },
  })
