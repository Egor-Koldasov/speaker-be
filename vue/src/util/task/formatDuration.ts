import type plugin from 'dayjs/plugin/duration'

export const formatDurationTime = (duration: plugin.Duration) => {
  const hours = duration.hours()
  const minutes = duration.minutes()
  const seconds = duration.seconds()
  const time = `${hours ? hours + 'h' : ''}${minutes ? minutes + 'm' : ''}${
    seconds ? seconds + 's' : ''
  }`
  return time
}

export const dayMs = 1000 * 60 * 60 * 24
