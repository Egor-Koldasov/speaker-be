import { timeout } from './timeout'

type WithTimeoutFn = (util: {
  resolve: () => void
  reject: (err: unknown) => void
}) => void

export const withTimeout = async <Fn extends WithTimeoutFn>(
  fn: Fn,
  timeoutMs: number,
) => {
  const timeoutController = timeout(timeoutMs)
  try {
    await new Promise<void>((resolve, reject) => {
      fn({ resolve, reject })
      timeoutController.promise.then(resolve).catch(reject)
    })
  } finally {
    timeoutController.cancel()
  }

  // const reject = (err: unknown) => {
  //   throw err
  // }
  // try {
  //   fn({ resolve: timeoutController.cancel, reject })
  //   await timeoutController.promise
  // } catch (err) {
  //   timeoutController.cancel()
  //   throw err
  // }
}
