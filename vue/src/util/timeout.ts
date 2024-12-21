export const timeout = (ms: number) => {
  let timer: NodeJS.Timeout
  let resolveFn: () => void

  const promise = new Promise<void>((resolve) => {
    resolveFn = resolve
    timer = setTimeout(resolve, ms)
  })

  return {
    promise,
    cancel: () => {
      clearTimeout(timer)
      resolveFn()
    },
  }
}
