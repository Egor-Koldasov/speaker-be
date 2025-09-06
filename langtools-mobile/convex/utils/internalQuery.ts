import { NoOp } from 'convex-helpers/server/customFunctions'
import { zCustomQuery } from 'convex-helpers/server/zod'
import { internalQuery as query_ } from '../_generated/server'

export const internalQuery = zCustomQuery(query_, NoOp)
