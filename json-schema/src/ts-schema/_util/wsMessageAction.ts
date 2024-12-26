import { JSONSchema7 } from "json-schema";
import WsMessageBase from "../ws-message/WsMessageBase";
import { SchemaObjectOpts, schemaObject } from "./schemaObject";
import { wsMessage } from "./wsMessage";
import ActionBase from "../ws-message/message/RequestToServer/Action/ActionBase";

type WsMessageBaseJSchema = typeof WsMessageBase;
type ActionBaseJSchema = typeof ActionBase;
type WsMessageJSchemaProps = Omit<
  WsMessageBaseJSchema["properties"],
  "id" | "errors" | "name" | "responseForId"
> & {
  name: {
    const: string;
  };
  responseForId?: {
    type: "string";
  };
};

type ActionDataBase = NonNullable<
  WsMessageJSchemaProps["data"]["properties"]
> & {
  actionName: {
    const: string;
  };
  actionParams?: {
    type: ["object"];
    properties?: JSONSchema7["properties"];
  };
};

export const wsMessageAction = <
  ActionData extends ActionDataBase,
  Opts extends SchemaObjectOpts & { relPathToWsMessage: string } & {
    response?: boolean;
  },
>(
  actionData: ActionData,
  opts: Opts
): ActionBaseJSchema => {
  const msgSchema = wsMessage(
    {
      name: {
        const: "Action",
      },
      data: schemaObject({
        actionParams: {
          type: ["object"],
        },
        ...actionData,
      }),
      responseForId: !opts.response ? undefined : { type: "string" },
    },
    opts
  );
  return msgSchema;
};
