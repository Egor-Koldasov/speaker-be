export const waitFor = async (condition: () => boolean, timeout = 30000) => {
  const start = Date.now()
  while (!condition() && Date.now() - start < timeout) {
    await new Promise((resolve) => setTimeout(resolve, 100))
  }
  if (!condition()) {
    throw new Error('waitFor timeout')
  }
}
