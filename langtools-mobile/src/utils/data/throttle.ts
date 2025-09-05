export const throttle = <T extends (...args: any[]) => void>(
  fn: T,
  ms: number,
) => {
  let lastCall = 0
  return (...args: Parameters<T>) => {
    const now = Date.now()
    if (now - lastCall >= ms) {
      lastCall = now
      fn(...args)
    }
  }
}

export const throttleAsync = <T extends (...args: any[]) => Promise<void>>(
  fn: T,
  ms: number,
) => {
  let lastCall = 0
  return async (...args: Parameters<T>) => {
    const now = Date.now()
    if (now - lastCall >= ms) {
      lastCall = now
      await fn(...args)
    }
  }
}
