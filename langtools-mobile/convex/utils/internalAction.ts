import { NoOp } from 'convex-helpers/server/customFunctions'
import { zCustomAction } from 'convex-helpers/server/zod'
import { internalAction as internalAction_ } from '../_generated/server'

export const internalAction = zCustomAction(internalAction_, NoOp)
