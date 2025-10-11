import { all as allLocales } from 'locale-codes'
import { FlatList, Pressable } from 'react-native'
import { View } from '../ui/View'
import { Text } from '../ui/Text'
import { styles } from '../../utils/styles/styles'
import { useStyles } from '../../utils/styles/useStyles'
import { useQuery } from 'convex/react'
import { api } from '../../../convex/_generated/api'
import { Button } from '../ui/Button'
import { Loading } from '../ui/Loading'
import { proxy, useSnapshot } from 'valtio'
import { TextInput } from '../ui/TextInput'
import { useMemo } from 'react'
import { useMutation } from '../../utils/convex/useMutation'

const state = proxy({
  languageSearch: '',
})

export function LearningLanguageSelector() {
  const styles = useStyles(getStyles)
  const snap = useSnapshot(state)

  const learningLanguage = useQuery(
    api.learningLanguage.getLearningLanguage,
    {},
  )
  const setCurrentLearningLanguage = useMutation(
    api.learningLanguage.setCurrentLearningLanguage,
  )

  const filteredLocales = useMemo(() => {
    if (!snap.languageSearch.trim()) return allLocales
    return allLocales.filter(
      (locale) =>
        locale.name
          .toLowerCase()
          .includes(snap.languageSearch.trim().toLowerCase()) ||
        locale.location
          ?.toLowerCase()
          .includes(snap.languageSearch.trim().toLowerCase()) ||
        locale.tag
          .toLowerCase()
          .includes(snap.languageSearch.trim().toLowerCase()),
    )
  }, [snap.languageSearch])

  if (learningLanguage === undefined) {
    return <Loading />
  }

  return (
    <View style={styles.learningLanguageSelector}>
      <View style={styles.currentLanguageBox}>
        <Text>Currently learning:</Text>
        <Button tone="secondary">
          {learningLanguage?.selectedLearningLanguage ?? 'None'}
        </Button>
      </View>
      <TextInput
        value={snap.languageSearch}
        onChangeText={(text) => (state.languageSearch = text)}
        placeholder="Search"
      />
      <FlatList
        style={styles.list}
        data={filteredLocales}
        renderItem={({ item: locale }) => (
          <Pressable
            key={locale.tag}
            style={styles.languageListItem}
            onPress={() => {
              setCurrentLearningLanguage.mutate({
                selectedLearningLanguage: locale.tag,
              })
            }}
          >
            <Text>
              {locale.name}
              {locale.location ? ` (${locale.location})` : ''}
            </Text>
            <Text>[{locale.tag}]</Text>
          </Pressable>
        )}
      />
    </View>
  )
}

const getStyles = styles((theme) => ({
  learningLanguageSelector: {
    gap: theme.spacing.sm,
  },
  list: {
    height: 200,
  },
  currentLanguageBox: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: theme.spacing.xs,
  },
  languageListItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    // paddingHorizontal: theme.spacing.xs,
    paddingVertical: theme.spacing.xxs / 2,
  },
}))
