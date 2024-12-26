import winston, { createLogger } from 'winston'

export const wsLogger = createLogger({
  level: 'info',
  transports: [new winston.transports.Console()],
  format: winston.format.combine(
    winston.format.label({ label: 'WebSocket' }),
    winston.format.timestamp(),
    winston.format.simple(),
  ),
})
