import { schemaObject } from "./_util/schemaObject";

export default schemaObject(
  {
    model: {
      $ref: "#/definitions/Models",
    },
    lensModel: {
      $ref: "#/definitions/LenseModels",
    },
    WsMessageType: {
      $ref: "./ws-message/WsMessageType.json",
    },
    WsMessageNameRequestToServer: {
      $ref: "./ws-message/WsMessageNameRequestToServer.json",
    },
    // WsMessageNameRequestFromServer: {
    //   $ref: "./ws-message/WsMessageNameRequestFromServer.json",
    // },
    WsMessageNameEventToServer: {
      $ref: "./ws-message/WsMessageNameEventToServer.json",
    },
    // WsMessageNameEventFromServer: {
    //   $ref: "./ws-message/WsMessageNameEventFromServer.json",
    // },
    WsMessageName: {
      $ref: "./ws-message/WsMessageName.json",
    },
    WsMessageBase: {
      $ref: "./ws-message/WsMessageBase.json",
    },
    WsMessage: schemaObject({
      RequestToServer: schemaObject({
        Action: schemaObject({
          ActionBase: {
            $ref: "./ws-message/message/RequestToServer/Action/ActionBase.json",
          },
          ActionName: {
            $ref: "./ws-message/message/RequestToServer/Action/ActionName.json",
          },
          SignUpByEmail: {
            $ref: "./ws-message/message/RequestToServer/Action/ActionSignUpByEmail.json",
          },
          SignUpByEmailResponse: {
            $ref: "./ws-message/message/RequestToServer/Action/ActionSignUpByEmailResponse.json",
          },
        }),
      }),
    }),
  },
  {
    title: "Main",
    $id: "Main",
    definitions: {
      MessageMap: schemaObject({
        ParseTextFromForeign: {
          $ref: "./model/MessageParseTextFromForeign.json",
        },
        DefineTerm: {
          $ref: "./model/MessageDefineTerm.json",
        },
        GetAuthInfo: {
          $ref: "./model/MessageGetAuthInfo.json",
        },
        GetDecks: {
          $ref: "./model/MessageGetDecks.json",
        },
        AddCard: {
          $ref: "./model/MessageAddCard.json",
        },
        GetCards: {
          $ref: "./model/MessageGetCards.json",
        },
      }),
      ChatGroupMap: schemaObject({
        ParseTextFromForeign: schemaObject({
          input: {
            $ref: "./model/ChatInputParseTextFromForeign.json",
          },
          output: {
            $ref: "./model/ChatOutputParseTextFromForeign.json",
          },
        }),
        DefineTerm: schemaObject({
          input: {
            $ref: "./model/ChatInputDefineTerm.json",
          },
          output: {
            $ref: "./model/ChatOutputDefineTerm.json",
          },
        }),
      }),
      LenseModels: {
        $ref: "./LenseModels.json",
      },
      Models: schemaObject({
        MessageBase: {
          $ref: "./model/MessageBase.json",
        },
        messages: {
          $ref: "#/definitions/MessageMap",
        },
        AuthSession: {
          $ref: "./model/AuthSession.json",
        },
        AuthInfo: {
          $ref: "./model/AuthInfo.json",
        },
        Card: {
          $ref: "./model/Card.json",
        },
        // CardType: {
        //   $ref: "./model/CardType.json",
        // },
      }),
    },
  }
);
