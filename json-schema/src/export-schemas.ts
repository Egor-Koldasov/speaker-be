import Ajv from "ajv";
import { writeFile } from "fs/promises";
import { compileFromFile } from "json-schema-to-typescript";
import path from "path";

const exportSchemas = async (ajv: Ajv) => {
  const types = await compileFromFile(
    path.resolve(__dirname, "../schema/Message.schema.json"),
    {
      cwd: path.resolve(__dirname, "../schema"),
    }
  );
  console.log(types);
  await writeFile(
    path.resolve(__dirname, "../../src/schema/Message.schema.ts"),
    types
  );
  await writeFile(
    path.resolve(__dirname, "../../vue/src/schema/Message.schema.ts"),
    types
  );
};

const main = async () => {
  const ajv = new Ajv();
  await exportSchemas(ajv);
};

main();