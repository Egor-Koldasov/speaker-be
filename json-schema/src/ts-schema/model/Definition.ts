import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    languageOriginal: {
      description: "The original language of the word in a BCP 47 format.",
    },
    languageTranslated: {
      type: "string",
      description: "The language the word is translated to in a BCP 47 format.",
    },
    originalWord: {
      type: "string",
      description:
        "The original word given, in the exact same grammatic form, capitalized.",
    },
    neutralForm: {
      type: "string",
      description: "The word in a neutral grammatic form.",
    },
    pronounciations: {
      type: "array",
      minItems: 1,
      items: schemaObject({
        transcription: {
          type: "string",
          description: "A pronunciation of the original word given.",
        },
        description: {
          type: "string",
          description:
            "A description of the pronunciation. Like the area where it is commonly used.",
        },
      }),
    },
    translation: {
      type: "string",
      description:
        "An extensive translation to the language defined by a `languageTranslated` property, the more words the better. In case of multiple meanings, include all of them.",
    },
    synonyms: {
      type: "array",
      items: {
        type: "string",
      },
      description: "Common synonyms in the original language.",
    },
    definitionOriginal: {
      type: "string",
      description: "An extensive definition in the original language.",
    },
    definitionTranslated: {
      type: "string",
      description:
        "An extensive definition in the language defined by a `languageTranslated` property.",
    },
    origin: {
      type: "string",
      description:
        "The root parts of the word and the origin in the language defined by a `languageTranslated` property. If the original form from Part 1 is different from the neutral grammatic form from Part 2, explain that difference including all the details.",
    },
    examples: {
      type: "array",
      items: schemaObject({
        original: {
          type: "string",
          description:
            "An example sentence in the original language using the word.",
        },
        translation: {
          type: "string",
          description:
            "The translation of the example sentence in the language defined by a `languageTranslated` property.",
        },
      }),
      description:
        "Three sentence examples of the usage of the original word in the same grammatic form followed by an translation in the language defined by a `languageTranslated` property. The sentence and the translation should be separated by one new line, while the examples themselves should be separated by three new lines. If there was a context from which that word was taken, include a phrase from that context in examples, replacing the first example.",
    },
  },
  {
    title: "Definition",
    description:
      "A detailed representation of a definition, including its original and neutral forms, pronunciations, translations, definitions, origin, and usage examples.",
    examples: [
      {
        originalWord: "Esperanzamos",
        neutralForm: "Esperanzar",
        pronounciations: [
          {
            transcription: "es.pe.ɾanˈθa.mos",
            description: "Spain",
          },
          {
            transcription: "es.pe.ɾanˈsa.mos",
            description: "Latin America",
          },
        ],
        translation:
          "To fill with hope, to become hopeful, to start to hope, to hold onto hope.",
        synonyms: ["Ilusionar", "tener esperanza", "confiar"],
        definitionOriginal:
          "Acción de hacerse llevar por la esperanza o comenzar a tener esperanza frente a una situación, a pesar de las circunstancias que pueden sugerir lo contrario.",
        definitionTranslated:
          "The action of being guided by or starting to have hope in a situation, despite circumstances that might suggest the contrary.",
        origin:
          'The verb "esperanzar" is derived from the noun "esperanza," meaning hope. The suffix "-ar" indicates that it\'s an infinitive verb. In this context, "esperanzamos" is the first person plural of the present indicative, meaning "we hope" or "we become hopeful." The transition from the neutral form "esperanzar" to "esperanzamos" changes the verb from its infinitive form to a specific tense and subject, indicating the action of hoping being performed by us in the present.',
        examples: [
          {
            original:
              "Y nos esperanzamos contra toda lógica, contra todo lo que nos dice la experiencia.",
            translation:
              "And we become hopeful against all logic, against everything our experience tells us.",
          },
          {
            original:
              "Cada vez que sale el sol, nos esperanzamos pensando que será un mejor día.",
            translation:
              "Every time the sun rises, we become hopeful thinking it will be a better day.",
          },
          {
            original:
              "A pesar de las dificultades, nos esperanzamos al ver la solidaridad de la gente.",
            translation:
              "Despite the difficulties, we become hopeful upon seeing people's solidarity.",
          },
        ],
      },
    ],
  }
);
