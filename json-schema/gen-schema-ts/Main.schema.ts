/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

/**
 * The unique identifier of the entity in uuid-v7 format
 */
export type Id = string;
/**
 * The code name of the error.
 */
export type ErrorName =
  | "Unknown"
  | "Internal"
  | "Ai_CreateCompletion"
  | "AI_ResponseUnmarshal"
  | "JsonSchema_MessageInput"
  | "JsonSchema_MessageOutput"
  | "NotFound_MessageName"
  | "FromAi_Critical";
/**
 * The list of BCP 47 language tags of the languages foreign to the user that are most commonly used in the learning process. Take this list as a priority when you try to detect the text language of the text foreign to the user. Although it is not guaranteed to completely match the text languages
 */
export type ForeignLanguages = string[];

export interface GenJsonSchema {
  model: Models;
}
export interface Models {
  MessageBase: MessageBase;
  messages: MessageMap;
}
export interface MessageBase {
  input: {
    id: Id;
    name: string;
    data: {
      [k: string]: unknown;
    };
  };
  output: {
    id: Id;
    name: string;
    data: {
      [k: string]: unknown;
    } | null;
    errors: AppError[];
  };
}
/**
 * An application typed error.
 */
export interface AppError {
  name: ErrorName;
  message: string;
}
export interface MessageMap {
  ParseTextFromForeign: MessageParseTextFromForeign;
  DefineTerm: MessageDefineTerm;
}
export interface MessageParseTextFromForeign {
  input: {
    id: Id;
    name: "ParseTextFromForeign";
    data: {
      text: string;
      originalLanguages: ForeignLanguages;
      translationLanguage: ForeignLanguages;
    };
  };
  output: {
    id: Id;
    name: "ParseTextFromForeign";
    data: {
      definitionParts: {
        /**
         * The text of word extracted. Keep this part small, it should not be longer than a typical dictionary entry point. Include only the word itself without any extra symbols. Do not include any punctuation symbols, enclosing parentheses or apostrophes an so on.
         */
        text: string;
        /**
         * A short translation of the word without additional formatting. Among several translation choices, choose the one that is the best fitting the original context from the user input text that was sent for this parsing.
         */
        translation: string;
        /**
         * The BCP 47 language tag of the language of that word. Null for unknown
         */
        languageOriginal: string;
        /**
         * The BCP 47 language tag of the language of the translation. It should match the requested 'translationLanguage'
         */
        languageTranslated: string;
      }[];
      /**
       * The full translation of the text to the requested language.
       */
      translation: {
        text: string;
        /**
         * The BCP 47 language tag of the language of the translation. It should match the requested 'translationLanguage'
         */
        language: string;
      };
    } | null;
    errors: AppError[];
  };
}
export interface MessageDefineTerm {
  input: {
    id: Id;
    name: "DefineTerm";
    data: {
      /**
       * A word or a common phrase to define
       */
      wordString: string;
      /**
       * A context from which the word or phrase is taken
       */
      context: string;
      originalLanguages: ForeignLanguages;
      /**
       * The BCP 47 language tag of the language that the user wants to translate the foreign text to.
       */
      translationLanguage: string;
    };
  };
  output: {
    id: Id;
    name: "DefineTerm";
    data: {
      definition: Definition;
    };
    errors: AppError[];
  };
}
/**
 * A detailed representation of a definition, including its original and neutral forms, pronunciations, translations, definitions, origin, and usage examples.
 */
export interface Definition {
  /**
   * The original language of the word in a BCP 47 format.
   */
  languageOriginal: {
    [k: string]: unknown;
  };
  /**
   * The language the word is translated to in a BCP 47 format.
   */
  languageTranslated: string;
  /**
   * The original word given, in the exact same grammatic form, capitalized.
   */
  originalWord: string;
  /**
   * The word in a neutral grammatic form.
   */
  neutralForm: string;
  /**
   * @minItems 1
   */
  pronounciations: [
    {
      /**
       * A pronunciation of the original word given.
       */
      transcription: string;
      /**
       * A description of the pronunciation. Like the area where it is commonly used.
       */
      description: string;
    },
    ...{
      /**
       * A pronunciation of the original word given.
       */
      transcription: string;
      /**
       * A description of the pronunciation. Like the area where it is commonly used.
       */
      description: string;
    }[]
  ];
  /**
   * An extensive translation to the language defined by a `languageTranslated` property, the more words the better. In case of multiple meanings, include all of them.
   */
  translation: string;
  /**
   * Common synonyms in the original language.
   */
  synonyms: string[];
  /**
   * An extensive definition in the original language.
   */
  definitionOriginal: string;
  /**
   * An extensive definition in the language defined by a `languageTranslated` property.
   */
  definitionTranslated: string;
  /**
   * The root parts of the word and the origin in the language defined by a `languageTranslated` property. If the original form from Part 1 is different from the neutral grammatic form from Part 2, explain that difference including all the details.
   */
  origin: string;
  /**
   * Three sentence examples of the usage of the original word in the same grammatic form followed by an translation in the language defined by a `languageTranslated` property. The sentence and the translation should be separated by one new line, while the examples themselves should be separated by three new lines. If there was a context from which that word was taken, include a phrase from that context in examples, replacing the first example.
   */
  examples: {
    /**
     * An example sentence in the original language using the word.
     */
    original: string;
    /**
     * The translation of the example sentence in the language defined by a `languageTranslated` property.
     */
    translation: string;
  }[];
}