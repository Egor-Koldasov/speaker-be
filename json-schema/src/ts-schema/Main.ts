import { schemaObject } from "./_util/schemaObject";

export default schemaObject(
  {
    model: {
      $ref: "#/definitions/Models",
    },
    LensModel: {
      $ref: "#/definitions/DbModels",
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
          SignUpByEmailCode: {
            $ref: "./ws-message/message/RequestToServer/Action/ActionSignUpByEmailCode.json",
          },
          SignUpByEmailCodeResponse: {
            $ref: "./ws-message/message/RequestToServer/Action/ActionSignUpByEmailCodeResponse.json",
          },
          CreateCardConfig: {
            $ref: "./ws-message/message/RequestToServer/Action/ActionCreateCardConfig.json",
          },
          CreateFieldConfig: {
            $ref: "./ws-message/message/RequestToServer/Action/ActionCreateFieldConfig.json",
          },
        }),
        LensQuery: schemaObject({
          LensQueryBase: {
            $ref: "./ws-message/message/RequestToServer/LensQuery/LensQueryBase.json",
          },
          LensQueryName: {
            $ref: "./ws-message/message/RequestToServer/LensQuery/LensQueryName.json",
          },
          LensQueryUser: {
            $ref: "./ws-message/message/RequestToServer/LensQuery/LensQueryUser.json",
          },
          LensQueryUserResponse: {
            $ref: "./ws-message/message/RequestToServer/LensQuery/LensQueryUserResponse.json",
          },
          LensQueryUserCardConfigs: {
            $ref: "./ws-message/message/RequestToServer/LensQuery/LensQueryUserCardConfigs.json",
          },
          LensQueryUserCardConfigsResponse: {
            $ref: "./ws-message/message/RequestToServer/LensQuery/LensQueryUserCardConfigsResponse.json",
          },
          LensQueryCardConfig: {
            $ref: "./ws-message/message/RequestToServer/LensQuery/LensQueryCardConfig.json",
          },
          LensQueryCardConfigResponse: {
            $ref: "./ws-message/message/RequestToServer/LensQuery/LensQueryCardConfigResponse.json",
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
      DbModels: {
        $ref: "./DbModels.json",
      },
      LensModels: {
        $ref: "./LensModels.json",
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
      AiJsonSchemas: schemaObject({
        AiDictionaryEntryConfig: {
          $ref: "./aiJsonSchemas/AiDictionaryEntryConfig.json",
        },
        AiTermNeutralList: {
          $ref: "./aiJsonSchemas/AiTermNeutralList.json",
        },
        AiContextTerm: {
          $ref: "./aiJsonSchemas/AiContextTerm.json",
        },
      }),
    },
  }
);
