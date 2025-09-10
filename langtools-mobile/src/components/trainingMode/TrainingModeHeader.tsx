import { useQuery } from 'convex/react'
import { StyleSheet } from 'react-native'
import { api } from '../../../convex/_generated/api'
import { FsrsProgressState } from '../../../convex/utils/schema/FsrsProgressState'
import { Theme } from '../../theme'
import { useStyles } from '../../utils/styles/useStyles'
import { Text } from '../ui/Text'
import { View } from '../ui/View'

export function TrainingModeHeader() {
  const fsrsDueStats = useQuery(api.fsrsProgress.getFsrsDueStats, {})
  const styles = useStyles(getStyles)
  if (!fsrsDueStats) {
    return null
  }

  return (
    <View style={styles.trainingModeHeader}>
      <Text>Words due</Text>
      <View style={styles.trainingModeStats}>
        <View>
          <Text style={styles.learningText}>
            {fsrsDueStats.fsrsProgressStateToCount[FsrsProgressState.Learning]}
          </Text>
        </View>
        <View>
          <Text style={styles.reviewText}>
            {fsrsDueStats.fsrsProgressStateToCount[FsrsProgressState.Review]}
          </Text>
        </View>
        <View>
          <Text style={styles.relearningText}>
            {
              fsrsDueStats.fsrsProgressStateToCount[
                FsrsProgressState.Relearning
              ]
            }
          </Text>
        </View>
      </View>
    </View>
  )
}

const getStyles = (theme: Theme) => {
  return StyleSheet.create({
    trainingModeHeader: {
      flexDirection: 'row',
      justifyContent: 'center',
      padding: theme.spacing.xs,
      marginHorizontal: theme.spacing.md,
      alignItems: 'center',
      borderRadius: theme.spacing.md,
      gap: theme.spacing.md,
      backgroundColor: theme.colors.surfaceElevated,
    },
    trainingModeStats: {
      flexDirection: 'row',
      gap: theme.spacing.md,
      alignItems: 'center',
    },
    learningText: {
      color: theme.colors.learning,
    },
    reviewText: {
      color: theme.colors.accent,
    },
    relearningText: {
      color: theme.colors.danger,
    },
  })
}
