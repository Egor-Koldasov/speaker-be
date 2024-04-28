import { mkdir, readdir, writeFile } from "fs/promises";
import { join } from "path";

import * as TJS from "typescript-json-schema";
import { createGenerator } from "ts-json-schema-generator";

const tsSchemaDir = join(__dirname, "../ts-schema");
type SchemaFile = {
  name: string;
  relPath: string;
  filePath: string;
};
export const getSchemaFiles = async (dir = ""): Promise<SchemaFile[]> => {
  const dirList = await readdir(join(tsSchemaDir, dir), {
    withFileTypes: true,
  });
  const schemaFiles = dirList.filter(
    (file) => file.isFile() && file.name.endsWith(".ts")
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
    ...schemaFiles.map((file) => ({
      name: file.name.split(".").slice(0, -1).join("."),
      relPath: dir,
      filePath: join(tsSchemaDir, dir, file.name),
    })),
    ...subDirFiles.flat(),
  ];
};

export const generateJsonSchema = async () => {
  const schemaFiles = await getSchemaFiles();
  // optionally pass argument to schema generator
  const settings: TJS.PartialArgs = {
    required: true,
    excludePrivate: true,
    constAsEnum: true,
    ref: true,
    aliasRef: true,
    topRef: true,
  };

  // optionally pass ts compiler options
  const compilerOptions: TJS.CompilerOptions = {};

  const program = TJS.getProgramFromFiles(
    schemaFiles.map((file) => file.filePath),
    compilerOptions
  );

  // ... or a generator that lets us incrementally get more schemas
  const generator = TJS.buildGenerator(program, settings);

  if (!generator) {
    throw new Error("No generator");
  }

  const refs = program.getProjectReferences();
  console.log(refs);

  await Promise.all(
    schemaFiles.map(async (file) => {
      const schema = createGenerator({
        path: file.filePath,
        expose: "export",
        discriminatorType: "json-schema",
      }).createSchema();

      console.log(schema);

      const mainSymbols = generator.getMainFileSymbols(program, [
        file.filePath,
      ]);

      if (mainSymbols.length !== 1) {
        throw new Error(
          "Expected exactly one type in schema file. " + file.name
        );
      }
      try {
        const schemaForFile = generator.getSchemaForSymbol(
          mainSymbols[0],
          true
        );
        schemaForFile.$id = join(file.relPath, file.name);
        schemaForFile.title = file.name;
        const schemaPath = join(__dirname, "../schema-gen", file.relPath);
        await mkdir(schemaPath, { recursive: true });
        await writeFile(
          join(schemaPath, `${file.name}.json`),
          JSON.stringify(schemaForFile, null, 2)
        );
      } catch (error) {
        console.error(error);
      }
      return mainSymbols;
    })
  );

  // const schemaForMainFile = generator.getSchemaForSymbol("models", true);

  // // generator can be also reused to speed up generating the schema if usecase allows:
  // const schemaWithReusedGenerator = TJS.generateSchema(
  //   program,
  //   "*",
  //   settings,
  //   undefined,
  //   generator
  // );
};

generateJsonSchema();
