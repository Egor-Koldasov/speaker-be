import type { Coord } from '../uiStore/useUisNodeMap'

export const getRectMid = (rect: DOMRect): Coord => ({
  x: rect.x + rect.width / 2,
  y: rect.y + rect.height / 2,
})
