export const rafX = (x: number, cb: () => unknown) => {
  requestAnimationFrame(() => {
    if (x <= 1) {
      cb()
      return
    }
    rafX(x - 1, cb)
  })
}
