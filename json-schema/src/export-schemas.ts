import $RefParser from "@apidevtools/json-schema-ref-parser";
import { mkdir, readdir, writeFile } from "fs/promises";
import { compileFromFile } from "json-schema-to-typescript";
import path, { join } from "path";

const tsSchemaDir = path.resolve(__dirname, "../dist/ts-schema");
const jsonSchemaDir = path.resolve(tsSchemaDir, "../../gen-schema-json");
const genBundleDir = path.resolve(tsSchemaDir, "../../gen-schema-bundle");
const genTsDir = path.resolve(tsSchemaDir, "../../gen-schema-ts");

export const getSchemaFiles = async (dir = ""): Promise<string[]> => {
  const dirList = await readdir(join(tsSchemaDir, dir), {
    withFileTypes: true,
  });
  const schemaFiles = dirList.filter(
    (file) => file.isFile() && file.name.endsWith(".js")
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
  const jsonSchemaPathList = await Promise.all(
    schemaFiles.map(async (schemaPath): Promise<string> => {
      const schema = require(join(tsSchemaDir, schemaPath)).default;
      const schemaString = JSON.stringify(schema, null, 2);
      const schemaPathJson = schemaPath.replace(/\.[^\.]+$/, ".json");
      const schemaJsonPath = path.resolve(jsonSchemaDir, schemaPathJson);
      await mkdir(path.dirname(schemaJsonPath), { recursive: true });
      await writeFile(schemaJsonPath, schemaString);

      return schemaPathJson;
    })
  );
  await Promise.all(
    jsonSchemaPathList.map(async (schemaPath): Promise<void> => {
      const schemaBundled = await $RefParser.bundle(
        join(jsonSchemaDir, schemaPath)
      );
      const bundlePath = path.resolve(genBundleDir, schemaPath);
      await mkdir(path.dirname(bundlePath), { recursive: true });
      await writeFile(bundlePath, JSON.stringify(schemaBundled, null, 2));
    })
  );
};

const exportSchemas = async () => {
  const types = await compileFromFile(
    path.resolve(jsonSchemaDir, "./Main.json"),
    {
      cwd: path.resolve(jsonSchemaDir),
    }
  );
  console.log(types);
  // await writeFile(
  //   path.resolve(__dirname, "../../src/schema/Main.schema.ts"),
  //   types
  // );
  await writeFile(path.resolve(genTsDir, "./Main.schema.ts"), types);
};

const main = async () => {
  await exportJsonSchemaBundles();
  await exportSchemas();
};

main();
