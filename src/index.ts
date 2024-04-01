import "dotenv/config";
import fastify, { FastifyReply } from "fastify";
import { components, operations, paths } from "./openapi";
import type { Handler, Request } from "openapi-backend";
import OpenAPIBackend from "openapi-backend";
import db from "./db";

type OperationId = keyof operations;

const api = new OpenAPIBackend({
  definition: "./openapi.ts",
});

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

type WordRow = {
  num: number;
  json: string;
};

type Word = components["schemas"]["Word"];

registerHandler("getWords", async (context, req, res: FastifyReply) => {
  const wordRows: WordRow[] = await db.select().from("words");
  const words: Word[] = [];
  for (const row of wordRows) {
    try {
      words.push(JSON.parse(row.json));
    } catch (e) {
      console.error(e);
    }
  }
  res.status(200);
});

app.listen({ port: 9000 }, () =>
  console.info("api listening at http://localhost:9000")
);
