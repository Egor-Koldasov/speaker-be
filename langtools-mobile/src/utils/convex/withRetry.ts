export type WithRetryOptions<Result> = {
  fn: () => Promise<Result>
  retries?: number
  delay?: number
  onRetry?: (error: unknown, attempt: number) => void
}

export const withRetry = async <Result>(
  opts: WithRetryOptions<Result>,
): Promise<Result> => {
  const { fn, retries = 3, delay = 1000, onRetry } = opts
  let attempt = 0
  while (attempt < retries) {
    try {
      return await fn()
    } catch (error) {
      onRetry?.(error, attempt)
      await new Promise((resolve) => setTimeout(resolve, delay))
      attempt++
    }
  }
  throw new Error('Max retries reached')
}
