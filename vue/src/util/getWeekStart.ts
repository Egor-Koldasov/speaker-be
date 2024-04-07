import dayjs from 'dayjs'

export const getWeekStart = (date?: number) => dayjs(date).startOf('isoWeek').valueOf()
