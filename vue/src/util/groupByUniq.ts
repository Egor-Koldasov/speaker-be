export const groupByUnique = <K extends string, T extends { [Key in K]: unknown }>(
  array: T[],
  key: K,
): Record<string, T> => {
  const uniqMap: Record<string, T> = {}
  array.forEach((item) => {
    uniqMap[String(item[key])] = item
  })
  return uniqMap
}
