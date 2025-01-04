export const waitFor = async (
  condition: () => boolean | Promise<boolean>,
  opts: {
    timeout?: number
    stepTimeout?: number
  } = {},
) => {
  const { timeout = 3000, stepTimeout = 100 } = opts
  const start = Date.now()
  let resolved = false
  while (!resolved && Date.now() - start < timeout) {
    resolved = await Promise.resolve(condition())
    if (!resolved) {
      await new Promise((resolve) => setTimeout(resolve, stepTimeout))
    }
  }
  if (!resolved) {
    throw new Error('waitFor timeout')
  }
}
