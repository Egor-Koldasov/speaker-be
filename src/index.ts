import "dotenv/config";
import fastify, { FastifyReply } from "fastify";
import type { Handler } from "openapi-backend";
import OpenAPIBackend from "openapi-backend";
import db from "./db";
import { components, operations } from "./openapi";

type OperationId = keyof operations;

const api = new OpenAPIBackend({
  definition: "./openapi.yml",
});
api.init();

const app = fastify({ logger: true });

app.route({
  method: ["GET", "POST", "PUT", "PATCH", "DELETE"],
  url: "/*",
  handler: async (request, reply) =>
    api.handleRequest(
      {
        method: request.method,
        path: request.url,
        body: request.body,
        query: request.query as any,
        headers: request.headers,
      },
      request,
      reply
    ),
});

const registerHandler = (operationId: OperationId, handler: Handler) => {
  api.registerHandler(operationId, handler);
};

type Word = components["schemas"]["Word"];

type WordRow = {
  num: number;
  json: Word;
};

registerHandler("getWords", async (context, req, res: FastifyReply) => {
  const wordRows: WordRow[] = await db.select().from("word");
  const words: Word[] = [];
  for (const row of wordRows) {
    try {
      words.push(row.json);
    } catch (e) {
      console.error(e);
    }
  }
  res.status(200).send(words);
});

app.listen({ port: 9000 }, () =>
  console.info("api listening at http://localhost:9000")
);
