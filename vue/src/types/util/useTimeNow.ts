import dayjs from "dayjs"
import { ref } from "vue"

export const useTimeNow = () => {
  const timeNow = ref(dayjs().valueOf())

  setInterval(() => {
    timeNow.value = dayjs().valueOf()
  }, 1000)

  return timeNow
}
