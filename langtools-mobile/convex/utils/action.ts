import { NoOp } from 'convex-helpers/server/customFunctions'
import { zCustomAction } from 'convex-helpers/server/zod'
import { action as action_ } from '../_generated/server'

export const action = zCustomAction(action_, NoOp)
