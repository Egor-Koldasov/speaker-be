// Create a random 4 character string
export const makeTestId = () => {
  return Math.random().toString(36).substring(2, 6)
}
