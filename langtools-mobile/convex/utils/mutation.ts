import { NoOp } from 'convex-helpers/server/customFunctions'
import { zCustomMutation } from 'convex-helpers/server/zod'
import { mutation as mutation_ } from '../_generated/server'

export const mutation = zCustomMutation(mutation_, NoOp)
