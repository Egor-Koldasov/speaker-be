import { createConsola } from 'consola'

const pino = createConsola({
  level: 5,
})

export const wsLogger = pino
