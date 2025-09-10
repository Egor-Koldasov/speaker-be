import { useMemo } from 'react'
import { Theme, useTheme } from '../../theme'

export const useStyles = <Styles>(getStyles: (theme: Theme) => Styles) => {
  const theme = useTheme()
  return useMemo(() => getStyles(theme), [getStyles, theme])
}
