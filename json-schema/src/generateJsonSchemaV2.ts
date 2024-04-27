import { resolve } from "path";

import * as TJS from "typescript-json-schema";

export const generateJsonSchema = async () => {
  // optionally pass argument to schema generator
  const settings: TJS.PartialArgs = {
    titles: true,
    required: true,
    excludePrivate: true,
  };

  // optionally pass ts compiler options
  const compilerOptions: TJS.CompilerOptions = {};

  const program = TJS.getProgramFromFiles(
    [resolve(__dirname, "../ts-schema/ts-schema.ts")],
    compilerOptions
  );

  // We can either get the schema for one file and one type...
  const schema = TJS.generateSchema(program, "*", settings);

  // ... or a generator that lets us incrementally get more schemas

  const generator = TJS.buildGenerator(program, settings);

  if (!generator) {
    throw new Error("No generator");
  }

  // generator can be also reused to speed up generating the schema if usecase allows:
  const schemaWithReusedGenerator = TJS.generateSchema(
    program,
    "*",
    settings,
    [],
    generator
  );

  // all symbols
  const symbols = generator.getUserSymbols();

  // Get symbols for different types from generator.
  // generator.getSchemaForSymbol("MyType");
  // generator.getSchemaForSymbol("AnotherType");

  return {
    schema,
    schemaWithReusedGenerator,
    symbols,
  };
};

generateJsonSchema();
