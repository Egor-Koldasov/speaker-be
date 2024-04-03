/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */

export interface paths {
    "/word": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations["getWords"];
        put?: never;
        post: operations["createWord"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/csv": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations["exportCSV"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** @description Example: {
         *       "originalWord": "Esperanzamos",
         *       "neutralForm": "Esperanzar",
         *       "pronounciation": "/es.pe.ɾanˈθa.mos/ (Spain), /es.pe.ɾanˈsa.mos/ (Latin America)",
         *       "translationEnglish": "To fill with hope, to become hopeful, to start to hope, to hold onto hope.",
         *       "synonyms": [
         *         "Ilusionar",
         *         "tener esperanza",
         *         "confiar"
         *       ],
         *       "definitionOriginal": "Acción de hacerse llevar por la esperanza o comenzar a tener esperanza frente a una situación, a pesar de las circunstancias que pueden sugerir lo contrario.",
         *       "definitionEnglish": "The action of being guided by or starting to have hope in a situation, despite circumstances that might suggest the contrary.",
         *       "origin": "The verb \"esperanzar\" is derived from the noun \"esperanza,\" meaning hope. The suffix \"-ar\" indicates that it's an infinitive verb. In this context, \"esperanzamos\" is the first person plural of the present indicative, meaning \"we hope\" or \"we become hopeful.\" The transition from the neutral form \"esperanzar\" to \"esperanzamos\" changes the verb from its infinitive form to a specific tense and subject, indicating the action of hoping being performed by us in the present.",
         *       "examples": [
         *         {
         *           "original": "Y nos esperanzamos contra toda lógica, contra todo lo que nos dice la experiencia.",
         *           "english": "And we become hopeful against all logic, against everything our experience tells us."
         *         },
         *         {
         *           "original": "Cada vez que sale el sol, nos esperanzamos pensando que será un mejor día.",
         *           "english": "Every time the sun rises, we become hopeful thinking it will be a better day."
         *         },
         *         {
         *           "original": "A pesar de las dificultades, nos esperanzamos al ver la solidaridad de la gente.",
         *           "english": "Despite the difficulties, we become hopeful upon seeing people's solidarity."
         *         }
         *       ]
         *     }
         *      */
        Word: {
            /** @description The original word given, in the exact same grammatic form, capitalized */
            originalWord: string;
            /** @description The word in a neutral grammatic form */
            neutralForm: string;
            /** @description A pronunciation of the original word given */
            pronounciation: string;
            /** @description An extensive translation to English, the more words the better */
            translationEnglish: string;
            /** @description Common synonyms in the original language */
            synonyms: string[];
            /** @description An extensive definition in the original language */
            definitionOriginal: string;
            /** @description An extensive definition in English */
            definitionEnglish: string;
            /** @description The root parts of the word and the origin in English. If the original form from Part 1 is different from the neutral grammatic form from Part 2, explain that difference including all the details. */
            origin: string;
            /** @description Three sentence examples of the usage of the original word in the same grammatic form followed by an English translation. The sentence and the translation should be separated by one new line, while the examples themselves should be separated by three new lines. If there was a context from which that word was taken, include a phrase from that context in examples, replacing the first example. */
            examples: {
                original?: string;
                english?: string;
            }[];
        };
    };
    responses: {
        /** @description Server error */
        ServerError: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                "application/json": {
                    /** @example Internal server error */
                    message?: string;
                };
            };
        };
    };
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    getWords: {
        parameters: {
            query?: {
                /** @description Number of words to return, default is 100 */
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description A list of words */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Word"][];
                };
            };
            500: components["responses"]["ServerError"];
        };
    };
    createWord: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Word"];
            };
        };
        responses: {
            /** @description Word created */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            500: components["responses"]["ServerError"];
        };
    };
    exportCSV: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Export words as CSV */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "text/csv": string;
                };
            };
            500: components["responses"]["ServerError"];
        };
    };
}
