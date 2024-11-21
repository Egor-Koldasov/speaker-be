import pino from 'pino'

export const wsLogger = pino({
  name: 'WebSocket',
  level: 'debug',
})
