import { NoOp } from 'convex-helpers/server/customFunctions'
import { zCustomMutation } from 'convex-helpers/server/zod'
import { internalMutation as mutation_ } from '../_generated/server'

export const internalMutation = zCustomMutation(mutation_, NoOp)
