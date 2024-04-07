export const runPromiseSequence = async (promiseFns: (() => Promise<unknown>)[]) => {
  const results: unknown[] = []
  for (const promiseFn of promiseFns) {
    results.push(await promiseFn())
  }
  return results
}
