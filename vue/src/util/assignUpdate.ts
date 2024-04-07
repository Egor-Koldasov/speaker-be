export const assignUpdate = <T extends object>(
  target: T,
  src: Partial<T>,
): T => {
  ;(Object.keys(src) as (keyof typeof src)[]).forEach((key) => {
    if (target[key] === src[key]) return
    target[key] = src[key]!
  })
  return target
}
