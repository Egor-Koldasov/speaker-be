import OpenAI from "openai";
import { operations } from "./openapi";
import openaiSchema from "../openapi-resolved.json";
import db, { dbOnError } from "./db";
import { uuidv7 } from "uuidv7";
import WordJsonSchema from "../json-schema/schema/Word.schema.json";
import MessageParseTextJsonSchema from "./json-schema-bundle/MessageParseText.schema.json";
import MessageDefineWordJsonSchema from "./json-schema-bundle/MessageDefineWord.schema.json";
import MessageParseTextToForeignJsonSchema from "./json-schema-bundle/MessageParseTextToForeign.schema.json";
import { MessageParseText } from "./schema/MessageUnion.schema";
import {
  MessageDefineWord,
  MessageParseTextToForeign,
  MessageTextToSpeech,
} from "./schema/Main.schema";

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

const instructionSplit = `
Handle the operation following the JSON schema.
Here's the description of the input that should be passed:
\`\`\`json
${JSON.stringify(MessageParseTextJsonSchema.properties.input, null, 2)}
\`\`\`
Generate a response following the instructions and the structure of this JSON schema:
\`\`\`json
${JSON.stringify(MessageParseTextJsonSchema.properties.output, null, 2)}
\`\`\`
`;

export const splitPhrase = async (
  data: MessageParseText["input"],
  force: boolean
) => {
  const operation_json = data;
  // if (!force) {
  //   const [operation] = await db
  //     .select()
  //     .from("history_ai")
  //     .orderBy("created_at", "desc")
  //     .limit(1)
  //     .whereRaw(
  //       `operation_json->>'name' = 'splitPhrase' AND operation_json#>>'{parameters,phrase}' = ?`,
  //       [phrase]
  //     );
  //   if (operation) {
  //     try {
  //       return operation.response_json.completion as OpenAI.ChatCompletion;
  //     } catch (error) {
  //       console.error(error);
  //     }
  //   }
  // }

  const completion = await openai.chat.completions.create({
    model: "gpt-4-1106-preview",
    messages: [
      {
        role: "system",
        content: JSON.stringify({
          instructions: instructionSplit,
        }),
      },
      {
        role: "user",
        content: JSON.stringify(data satisfies MessageParseText["input"]),
      },
    ],
    n: 1,
    response_format: {
      type: "json_object",
    },
  });

  console.log("splitPhrase", JSON.stringify({ completion }));

  db("history_ai")
    .insert({
      id: uuidv7(),
      operation_json: JSON.stringify(operation_json),
      response_json: JSON.stringify(completion),
    })
    .then()
    .catch(dbOnError);

  return completion;
};

const instructionsDefineWord = `
Handle the operation following the JSON schema.
Here's the description of the input that should be passed:
\`\`\`json
${JSON.stringify(MessageDefineWordJsonSchema.properties.input, null, 2)}
\`\`\`
Define the word given the data provided.
Your response to that action will be a translation and definition reference for a particular word given.
Generate a response following the instructions and the structure of this JSON schema:
\`\`\`json
${JSON.stringify(MessageDefineWordJsonSchema.properties.output, null, 2)}
\`\`\`
`;

const instructionsParseTextToForeign = `
Handle the operation following the JSON schema.
Here's the description of the input that should be passed:
\`\`\`json
${JSON.stringify(MessageParseTextToForeignJsonSchema.properties.input, null, 2)}
\`\`\`
Translate the text from the language native to the user to a foreign language.
Besides the direct translation, give translations that are more natural to the foreign language specified.
Generate a response following the instructions and the structure of this JSON schema:
\`\`\`json
${JSON.stringify(
  MessageParseTextToForeignJsonSchema.properties.output,
  null,
  2
)}
\`\`\`
`;

export const defineWord = async (
  data: MessageDefineWord["input"],
  force: boolean
) => {
  const operation_json = data;
  // if (!force) {
  //   const [operation] = await db
  //     .select()
  //     .from("history_ai")
  //     .orderBy("created_at", "desc")
  //     .limit(1)
  //     .whereRaw(
  //       `operation_json->>'name' = 'defineWord' AND operation_json#>>'{parameters,wordString}' = ?`,
  //       [wordString]
  //     );
  //   if (operation) {
  //     try {
  //       return operation.response_json.completion as OpenAI.ChatCompletion;
  //     } catch (error) {
  //       console.error(error);
  //     }
  //   }
  // }

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
        role: "user",
        content: JSON.stringify(data),
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
      operation_json: JSON.stringify(operation_json),
      response_json: JSON.stringify({ completion }),
    })
    .then()
    .catch(dbOnError);

  return completion;
};

export const parseTextToForeign = async (
  data: MessageParseTextToForeign["input"]
) => {
  const completion = await openai.chat.completions.create({
    model: "gpt-4-1106-preview",
    messages: [
      {
        role: "system",
        content: JSON.stringify({
          instructions: instructionsParseTextToForeign,
        }),
      },
      {
        role: "user",
        content: JSON.stringify(data),
      },
    ],
    n: 1,
    response_format: {
      type: "json_object",
    },
  });
  return completion;
};

export const textToSpeech = async (input: MessageTextToSpeech["input"]) => {
  const audio = await openai.audio.speech.create({
    model: "tts-1",
    voice: "nova",
    input: input.data.text,
  });
  const base64 = Buffer.from(await audio.arrayBuffer()).toString("base64");
  return base64;
};
