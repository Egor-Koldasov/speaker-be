import "dotenv/config";
import fastify, { FastifyReply, FastifyRequest } from "fastify";
import type { Handler } from "openapi-backend";
import OpenAPIBackend from "openapi-backend";
import db from "./db";
import { components, operations } from "./openapi";
import { stringify } from "csv-stringify/sync";
import { createReadStream } from "fs";
import path = require("path");
import addFormats from "ajv-formats";
import { openai, splitPhrase, test } from "./ai";
import cors from "@fastify/cors";
import Ajv from "ajv";
import { readFile, readdir } from "fs/promises";
import { MessageUnion } from "./schema/MessageUnion.schema";
import { handleMesasge } from "./message";

type OperationId = keyof operations;

const api = new OpenAPIBackend({
  definition: "./openapi.yml",
  customizeAjv: (ajv) => {
    addFormats(ajv, {
      mode: "fast",
      formats: ["email", "uri", "date-time", "uuid"],
    });

    return ajv;
  },
});
api.init();

const app = fastify({ logger: true });

app.register(cors, {
  origin: "*",
  methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
});

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

registerHandler(
  "createWord",
  async (context, req: FastifyRequest, res: FastifyReply) => {
    const word = req.body as Word;
    const [num] = await db("word").insert({ json: word }).returning("num");
    res.status(201).send({ num });
  }
);

registerHandler(
  "exportCSV",
  async (context, req: FastifyRequest, res: FastifyReply) => {
    const params = req.query as operations["exportCSV"]["parameters"]["query"];
    const wordRows: WordRow[] = await db
      .select()
      .from("word")
      .whereRaw(
        `json::jsonb ->> 'languageOriginal' = $1 and json::jsonb ->> 'languageTranslated' = $2`,
        [params.languageOriginal, params.languageTranslated]
      )
      .whereRaw(`not json::jsonb ? 'csvExportedAt'`);
    const csv = stringify(
      wordRows.map(({ json }) => [
        json.originalWord,
        json.neutralForm,
        json.pronounciation,
        json.translation,
        json.synonyms.join(", "),
        json.definitionOriginal,
        json.definitionTranslated,
        json.origin,
        json.examples
          .map((example) => `${example.original}\n${example.translation}`)
          .join("\n\n\n"),
      ]),
      {
        header: false,
      }
    );
    const fileName = `words-${params.languageOriginal}-${
      params.languageTranslated
    }-${new Date().toISOString()}.csv`;
    res.header("Content-Type", "text/csv");
    res
      .header(`Content-Disposition`, `attachment; filename=${fileName}`)
      .send(csv);

    const updatedWordIds = wordRows.map(({ num }) => num);
    await db("word")
      .update({ csvExportedAt: new Date() })
      .whereIn("num", updatedWordIds);
    console.log(`Exported ${updatedWordIds.length} words`);
  }
);

app.get("/openapi", async (req, res) => {
  const stream = createReadStream(
    path.resolve(__dirname, "../../openapi-resolved.yml")
  );
  return res.type("application/yaml").send(stream);
});

app.get("/health", async (req, res) => {
  openai;
  const completion = await test();
  return res.status(200).send({ status: "ok", message: completion.choices[0] });
});

app.post("/text", async (req, res) => {
  const body = req.body as { text: string };
  const completion = await splitPhrase(body.text);
  return res.status(200).send(completion.choices[0]);
});

app.post("/message", async (req, res) => {
  const ajv = new Ajv();
  addFormats(ajv, {
    mode: "fast",
    formats: ["email", "uri", "date-time", "uuid"],
  });
  const fileNames = await readdir(
    path.resolve(__dirname, "../json-schema/schema")
  );
  await Promise.all(
    fileNames.map(async (fileName) => {
      const schemaString = await readFile(
        path.resolve(__dirname, `../json-schema/schema/${fileName}`),
        "utf-8"
      );
      const schema = JSON.parse(schemaString);
      ajv.addSchema(schema, fileName);
    })
  );
  const messageValidator = ajv.getSchema("MessageUnion.schema.json");
  const valid = await messageValidator(req.body);
  console.log(valid);
  if (!valid) {
    console.log(messageValidator.errors);
    return res.status(400).send(messageValidator.errors);
  }
  const message = req.body as MessageUnion;
  const result = await handleMesasge(message);
  return res.status(200).send(result);
});

app.listen({ port: 9000 }, (error) =>
  error
    ? console.error(error)
    : console.info("api listening at http://localhost:9000")
);
