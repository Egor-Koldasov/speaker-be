import makeKnex from "knex";

const db = makeKnex({
  client: "pg",
  connection: process.env.PG_CONNECTION_STRING,
});

export const dbOnError = async (error: unknown) => {
  console.error("Database error:", error);
};

export default db;
