import { RegisteredQuery } from 'convex/server'

export type RegisteredQueryReturnType<
  Query extends RegisteredQuery<any, any, any>,
> = Query extends RegisteredQuery<any, any, infer Returns> ? Returns : never
