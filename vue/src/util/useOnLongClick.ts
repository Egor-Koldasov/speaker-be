import { ref } from 'vue'

export const useOnLongClick = (callback: () => void, ms = 500) => {
  const clickHolding = ref(false)
  const onHold = () => {
    clickHolding.value = true
    callback()
  }
  let timer: ReturnType<typeof setTimeout>
  const clearTimer = () => {
    if (timer) clearTimeout(timer)
    clickHolding.value = false
  }
  const startTimer = () => {
    clearTimer()
    timer = setTimeout(onHold, ms)
  }
  return {
    onMouseDown: startTimer,
    onMouseUp: clearTimer,
    onMouseLeave: clearTimer,
    clickHolding,
  }
}
