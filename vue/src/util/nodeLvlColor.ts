const colorLvls = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'violet']

export function nodeLvlColor(lvl: number): string {
  if (lvl < 0) return colorLvls[colorLvls.length - (lvl % colorLvls.length)]
  return colorLvls[lvl % colorLvls.length]
}
