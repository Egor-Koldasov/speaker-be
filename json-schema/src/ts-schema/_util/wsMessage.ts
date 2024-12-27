import { join } from "path";
import WsMessageBase from "../ws-message/WsMessageBase";
import { SchemaObjectOpts, schemaObject } from "./schemaObject";

type WsMessageBaseJSchema = typeof WsMessageBase;
type WsMessageJSchemaProps = Omit<
  WsMessageBaseJSchema["properties"],
  "id" | "errors" | "name" | "responseForId" | "authToken"
> & {
  name: {
    const: string;
  };
  responseForId?: {
    type: "string";
  };
};

export const wsMessage = <
  Props extends WsMessageJSchemaProps,
  Opts extends SchemaObjectOpts & { relPathToWsMessage: string } & {
    response?: boolean;
  },
>(
  props: Props,
  opts: Opts
): WsMessageBaseJSchema => {
  const msgSchema = schemaObject(
    {
      ...WsMessageBase.properties,
      errors: {
        type: "array",
        items: {
          $ref: join(opts.relPathToWsMessage, "../property/AppError.json"),
        },
      },
      ...props,
    },
    {
      ...opts,
      optional: opts.response ? [] : ["responseForId"],
    }
  );
  if (!msgSchema.title) {
    throw new Error("Title is required");
  }
  const msgSchemaWithTitle = {
    ...msgSchema,
    title: msgSchema.title ?? "",
  };
  return msgSchemaWithTitle;
};
