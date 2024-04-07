import { Pool } from 'pg'
import { Kysely, PostgresDialect } from 'kysely'

export type Database = {
  category: {
    id: string
    user_id: string
    color: string
    name: string
    created_at: string
  }
  task: {
    id: string
    created_at: string
    name: string
    type: string
    estimate: number
    note: string
    category_id: string
    status: string
    user_id: string
  }
  user: {
    id: string
    email: string
    created_at: string
    updated_at: string
  }
  node: {
    id: string
    user_id: string
    content_short: string
    content_long: string
    created_at: string
    updated_at: string
  }
  node_rel: {
    node_from_id: string
    node_to_id: string
  }
  alarm: {
    id: string
    date_end: string
  }
  status_manager: {
    id: string
    user_id: string
    root_node_id: string
    created_at: string
    updated_at: string
    deleted_at: string
  }
  status: {
    id: string
    manager_id: string
    node_id: string
    created_at: string
    updated_at: string
    deleted_at: string
  }
}

const dialect = new PostgresDialect({
  pool: new Pool({
    database: 'pttcat',
    host: 'localhost',
    user: 'admin',
    password: 'devpassword',
    port: 5434,
    ssl: false,
  }),
})

// Database interface is passed to Kysely's constructor, and from now on, Kysely
// knows your database structure.
// Dialect is passed to Kysely's constructor, and from now on, Kysely knows how
// to communicate with your database.
export const db = new Kysely<Database>({
  dialect,
})
