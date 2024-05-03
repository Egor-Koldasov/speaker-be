import $RefParser from "@apidevtools/json-schema-ref-parser";
import Ajv from "ajv";
import { mkdir, readdir, writeFile } from "fs/promises";
import { compileFromFile } from "json-schema-to-typescript";
import path, { join } from "path";

const tsSchemaDir = path.resolve(__dirname, "../schema-v2");

export const getSchemaFiles = async (dir = ""): Promise<string[]> => {
  const dirList = await readdir(join(tsSchemaDir, dir), {
    withFileTypes: true,
  });
  const schemaFiles = dirList.filter(
    (file) => file.isFile() && file.name.endsWith(".json")
  );
  const subDirs = dirList
    .filter((file, index) => file.isDirectory())
    .filter((file) => !file.name.startsWith("_"));
  const subDirFiles = await Promise.all(
    subDirs.map(async (subDir) => {
      const files = await getSchemaFiles(join(dir, subDir.name));
      return files;
    })
  );
  return [
    ...schemaFiles.map((file) => join(dir, file.name)),
    ...subDirFiles.flat(),
  ];
};

const exportJsonSchemaBundles = async () => {
  const schemaFiles = await getSchemaFiles();
  await Promise.all(
    schemaFiles.map(async (schemaPath): Promise<void> => {
      const schemaBundled = await $RefParser.bundle(
        join(tsSchemaDir, schemaPath)
      );
      const bundlePath = path.resolve(
        tsSchemaDir,
        "../gen-schema-bundle",
        schemaPath
      );
      await mkdir(path.dirname(bundlePath), { recursive: true });
      await writeFile(bundlePath, JSON.stringify(schemaBundled, null, 2));
    })
  );
};

const exportSchemas = async (ajv: Ajv) => {
  const types = await compileFromFile(
    path.resolve(tsSchemaDir, "./Main.json"),
    {
      cwd: path.resolve(tsSchemaDir),
    }
  );
  console.log(types);
  // await writeFile(
  //   path.resolve(__dirname, "../../src/schema/Main.schema.ts"),
  //   types
  // );
  await writeFile(
    path.resolve(tsSchemaDir, "../gen-schema-ts/Main.schema.ts"),
    types
  );

  await exportJsonSchemaBundles();
};

const main = async () => {
  const ajv = new Ajv();
  await exportSchemas(ajv);
};

main();
