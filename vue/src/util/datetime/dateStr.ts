import dayjs from 'dayjs'

export const dateStr = (...args: Parameters<typeof dayjs>) => dayjs(...args).toISOString()
