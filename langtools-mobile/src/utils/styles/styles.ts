import { StyleSheet } from 'react-native'
import { Theme } from '../../theme'

export const styles =
  <Styles extends StyleSheet.NamedStyles<Styles> | StyleSheet.NamedStyles<any>>(
    getStyles: (theme: Theme) => Styles,
  ) =>
  (theme: Theme) =>
    StyleSheet.create(getStyles(theme))
