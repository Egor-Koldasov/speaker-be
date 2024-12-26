export const waitFor = async (
  condition: () => boolean | Promise<boolean>,
  opts: {
    timeout?: number
    stepTimeout?: number
  } = {},
) => {
  const { timeout = 3000, stepTimeout = 100 } = opts
  const start = Date.now()
  while (
    !(await Promise.resolve(condition())) &&
    Date.now() - start < timeout
  ) {
    await new Promise((resolve) => setTimeout(resolve, stepTimeout))
  }
  if (!(await Promise.resolve(condition()))) {
    throw new Error('waitFor timeout')
  }
}
