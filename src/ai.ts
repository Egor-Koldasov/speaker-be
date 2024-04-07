import OpenAI from "openai";
import { operations } from "./openapi";
import openaiSchema from "../openapi-resolved.json";

const CreateWord = openaiSchema.paths["/word"].post;

const instructions = `
Let's create an action, with the technical name "DefineWord".
Your response to that action will be a translation and definition reference for a particular word given.
Let's define what the reference should contain:

1. The original word given, in the exact same grammatic form, capitalized.
2. The word in a neutral grammatic form
3. A pronunciation of the original word given
4. An extensive translation to English, the more words the better
5. Common synonyms in the original language
6. An extensive definition in the original language
7. An extensive definition in English
8. The root parts of the word and the origin in English. If the original form from Part 1 is different from the neutral grammatic form from Part 2, explain that difference including all the details.
9. Three sentence examples of the usage of the original word in the same grammatic form followed by an English translation. The sentence and the translation should be separated by one new line, while the examples themselves should be separated by three new lines. If there was a context from which that word was taken, include a phrase from that context in examples, replacing the first example.

An example:
\`\`\`text
1. Original word given: Esperanzamos
2. A neutral grammatic form: Esperanzar
3. Pronunciation: /es.pe.ɾanˈθa.mos/ (Spain), /es.pe.ɾanˈsa.mos/ (Latin America)
4. English translation: To fill with hope, to become hopeful, to start to hope, to hold onto hope.
5. Synonyms: Ilusionar, tener esperanza, confiar.
6. Definition in the original language: Acción de hacerse llevar por la esperanza o comenzar a tener esperanza frente a una situación, a pesar de las circunstancias que pueden sugerir lo contrario.
7. Definition in English: The action of being guided by or starting to have hope in a situation, despite circumstances that might suggest the contrary.
8. Roots and origins: The verb "esperanzar" is derived from the noun "esperanza," meaning hope. The suffix "-ar" indicates that it's an infinitive verb. In this context, "esperanzamos" is the first person plural of the present indicative, meaning "we hope" or "we become hopeful." The transition from the neutral form "esperanzar" to "esperanzamos" changes the verb from its infinitive form to a specific tense and subject, indicating the action of hoping being performed by us in the present.
9. Examples:
Y nos esperanzamos contra toda lógica, contra todo lo que nos dice la experiencia.
And we become hopeful against all logic, against everything our experience tells us.


Cada vez que sale el sol, nos esperanzamos pensando que será un mejor día.
Every time the sun rises, we become hopeful thinking it will be a better day.


A pesar de las dificultades, nos esperanzamos al ver la solidaridad de la gente.
Despite the difficulties, we become hopeful upon seeing people's solidarity.
\`\`\`

Each time you deduce from a message a need to define a word, execute this action for that word. Also, every call should be followed by the call of the API action "createWord".
If language is not specified, try to imply it from the context and execute the action using the implied language. Indicate in your response if you are unclear about the language used.
When working with sentences, don't execute this action against the whole sentence. Split it and do it only for single words or famous phrases. Also, do not implicitly execute it multiple times per message, instead ask me how I would like to continue.

Sounds good?
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

export const splitPhrase = async (phrase: string) => {
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
    response_format: {
      type: "json_object",
    },
  });
  return completion;
};
