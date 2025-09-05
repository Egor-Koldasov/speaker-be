import { NoOp } from 'convex-helpers/server/customFunctions'
import { zCustomQuery } from 'convex-helpers/server/zod'
import { query as query_ } from '../_generated/server'

export const query = zCustomQuery(query_, NoOp)
