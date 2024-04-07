import colorContrast from 'color-contrast'

const colors = ['#000', '#fff']

export const getContrastColor = (color: string) => {
  const contrast = colors.sort((a, b) => colorContrast(color, b) - colorContrast(color, a))[0]

  if (colorContrast(color, colors[0]) === 1) {
    console.warn(`Couldn't find contrast color for ${color}`)
  }

  return contrast
}
