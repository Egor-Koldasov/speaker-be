export const assignCopy = <T extends object>(target: T, src: T): T => {
  ;(Object.keys(src) as (keyof typeof src)[]).forEach((key) => {
    const targetValue = target[key]
    if (!(key in src)) {
      delete target[key]
      return
    }
    if (targetValue === src[key]) return
    if (
      typeof targetValue === 'object' &&
      targetValue &&
      typeof src[key] === 'object' &&
      src[key]
    ) {
      return assignCopy(targetValue, src[key] as typeof targetValue)
    }
    target[key] = src[key]
  })
  const deletedKeys = Object.keys(target).filter((key) => !(key in src)) as (keyof typeof target)[]
  deletedKeys.forEach((key) => {
    delete target[key]
  })
  return target
}
