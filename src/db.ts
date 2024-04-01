import makeKnex from "knex";

const db = makeKnex({
  client: "pg",
  connection: process.env.PG_CONNECTION_STRING,
});

export default db;
