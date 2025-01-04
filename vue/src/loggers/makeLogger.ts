import { pino } from 'pino'

export const makeLogger = (name: string) =>
  pino({
    name,
    formatters: {
      level(label, number) {
        return { level: [number, label] }
      },
    },
    // transport: {
    //   target: 'pino-pretty',
    //   options: {
    //     colorize: true,
    //   },
    // },
  })
