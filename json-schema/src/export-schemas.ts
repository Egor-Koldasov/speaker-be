import $RefParser from "@apidevtools/json-schema-ref-parser";
import Ajv from "ajv";
import { writeFile } from "fs/promises";
import { compileFromFile } from "json-schema-to-typescript";
import path from "path";

const jsonSchemasToBundle = [
  "MessageDefineWord.schema.json",
  "MessageParseText.schema.json",
  "MessageParseTextToForeign.schema.json",
  "MessageTextToSpeech.json",
];

const exportJsonSchemaBundles = async () => {
  await Promise.all(
    jsonSchemasToBundle.map(async (schemaName) => {
      const schemaBundled = await $RefParser.bundle(
        path.resolve(__dirname, "../schema", schemaName)
      );
      await writeFile(
        path.resolve(__dirname, "../../src/json-schema-bundle", schemaName),
        JSON.stringify(schemaBundled, null, 2)
      );
    })
  );
};

const exportSchemas = async (ajv: Ajv) => {
  const types = await compileFromFile(
    path.resolve(__dirname, "../schema/Main.schema.json"),
    {
      cwd: path.resolve(__dirname, "../schema"),
    }
  );
  console.log(types);
  await writeFile(
    path.resolve(__dirname, "../../src/schema/Main.schema.ts"),
    types
  );
  await writeFile(
    path.resolve(__dirname, "../../vue/src/schema/Main.schema.ts"),
    types
  );

  await exportJsonSchemaBundles();
};

const main = async () => {
  const ajv = new Ajv();
  await exportSchemas(ajv);
};

main();
