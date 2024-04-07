import dayjs from 'dayjs'
import { formatDurationTime, dayMs } from '../task/formatDuration'

export const formatDuration = (duration: number, zero = '0') => {
  const durationDelta = duration < 0 ? -duration : duration
  if (durationDelta === 0) return zero
  const durationDjs = dayjs.duration(durationDelta)
  const time = formatDurationTime(durationDjs)
  if (durationDelta < dayMs) return (duration < 0 ? '-' : '') + time
  const days = durationDjs.days()
  const months = durationDjs.months()
  const years = durationDjs.years()
  const date = `${years ? years + 'y' : ''}${months ? months + 'M' : ''}${days ? days + 'd' : ''}`
  return [duration < 0 ? '-' : '', date, time].join(' ')
}
