import { AppError } from "../property/AppError";
import { MessageBase } from "./MessageBase";

export interface MessageParseTextFromForeign extends MessageBase {
  input: {
    name: "ParseTextFromForeign";
    data: {
      text: string;
      originalLanguages: string[];
      /**
       * The BCP 47 language tag of the language that the user wants to translate the text to.
       */
      translationLanguage: string;
    };
  };
  /**
   * The result of parsing the text for futher translation.
   */
  output: {
    name: "ParseTextFromForeign";
    /**
     * Split the text into grammatical parts. A part should be a dictionary entry like a single word or a famous phrase, it is something that can be defined or translated. Do not include symbols, unless they are the integral part of a phrase.
     */
    data: {
      definitionParts: {
        /**
         * The text of the part split. Keep this part small, it should not be longer than a typical dictionary entry point. Usualy a single word or sometimes a single word or a famous phrase. Do not include any punctuation symbols, enclosing parentheses or apostrophes an so on.
         */
        text: string;
        /**
         * A short translation of the definition part without additional formatting. Among several translation choices, choose the one that is the best fitting the original context from the user input text that was sent for this parsing.
         */
        translation?: string;
        /**
         * The BCP 47 language tag of the language of that part. Null for unknown
         */
        languageOriginal?: string | null;
        /**
         * The BCP 47 language tag of the language of the translation. It should match the requested 'translationLanguage'
         */
        languageTranslated?: string;
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
