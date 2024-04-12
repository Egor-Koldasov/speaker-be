import OpenAI from "openai";
import { operations } from "./openapi";
import openaiSchema from "../openapi-resolved.json";
import db from "./db";
import { uuidv7 } from "uuidv7";
import WordJsonSchema from "../json-schema/schema/Word.schema.json";

const CreateWord = openaiSchema.paths["/word"].post;

const instructions = `
Let's create an action, with the technical name "DefineWord".
Your response to that action will be a translation and definition reference for a particular word given.
You should response with a JSON object, following this schema:
\`\`\`json
${JSON.stringify(WordJsonSchema, null, 2)}
\`\`\`
`;

export const openai = new OpenAI();

export const test = async () => {
  const completion = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [
      {
        role: "system",
        content: instructions,
      },
    ],
    tools: [
      {
        type: "function",
        function: {
          name: "createWord",
          parameters: openaiSchema.components.schemas.Word,
        },
      },
    ],
    n: 1,
  });
  return completion;
};

const instructionSplit = (phrase: string) =>
  `
Split the text into grammatical parts. A part can be a single word or a famous phrase,
it is something that can be defined or translated. Do not include symbols, unless they are the integral part of a phrase. Output the result as an array of strings and put
that inside a JSON object with the key "parts".
Here is the text to split:
\`\`\`
${phrase}
\`\`\`
`;

export const splitPhrase = async (phrase: string, force: boolean) => {
  const operation_json = {
    name: "splitPhrase",
    parameters: {
      phrase: phrase,
    },
  };
  if (!force) {
    const [operation] = await db
      .select()
      .from("history_ai")
      .orderBy("created_at", "desc")
      .limit(1)
      .whereRaw(
        `operation_json->>'name' = 'splitPhrase' AND operation_json#>>'{parameters,phrase}' = ?`,
        [phrase]
      );
    if (operation) {
      try {
        return operation.response_json.completion as OpenAI.ChatCompletion;
      } catch (error) {
        console.error(error);
      }
    }
  }

  const completion = await openai.chat.completions.create({
    model: "gpt-4-1106-preview",
    messages: [
      {
        role: "system",
        content: JSON.stringify({
          instructions: instructionSplit(phrase),
        }),
      },
    ],
    n: 1,
    response_format: {
      type: "json_object",
    },
  });

  db("history_ai")
    .insert({
      id: uuidv7(),
      operation_json: operation_json,
      response_json: JSON.stringify({ completion }),
    })
    .then();

  return completion;
};

const instructionsDefineWord = `
Let's create an action, with the technical name "DefineWord".
Your response to that action will be a translation and definition reference for a particular word given.
You should response with a JSON object that will contain the object property "word".
The structure of the "word" object and additional instructions are defined in this JSON schema:
\`\`\`json
${JSON.stringify(WordJsonSchema, null, 2)}
\`\`\`
If you cannot define the word given the data provided, set the "word" object to null, and provide an error in the "error" property as string.
`;

export const defineWord = async (wordString: string, force: boolean) => {
  const operation_json = {
    name: "defineWord",
    parameters: {
      wordString,
    },
  };
  if (!force) {
    const [operation] = await db
      .select()
      .from("history_ai")
      .orderBy("created_at", "desc")
      .limit(1)
      .whereRaw(
        `operation_json->>'name' = 'defineWord' AND operation_json#>>'{parameters,wordString}' = ?`,
        [wordString]
      );
    if (operation) {
      try {
        return operation.response_json.completion as OpenAI.ChatCompletion;
      } catch (error) {
        console.error(error);
      }
    }
  }

  const completion = await openai.chat.completions.create({
    model: "gpt-4-1106-preview",
    messages: [
      {
        role: "system",
        content: JSON.stringify({
          instructions: instructionsDefineWord,
        }),
      },
      {
        role: "system",
        content: JSON.stringify({
          action: "DefineWord",
          wordString,
          language: "de",
        }),
      },
    ],
    n: 1,
    response_format: {
      type: "json_object",
    },
  });

  db("history_ai")
    .insert({
      id: uuidv7(),
      operation_json: operation_json,
      response_json: JSON.stringify({ completion }),
    })
    .then();

  return completion;
};
