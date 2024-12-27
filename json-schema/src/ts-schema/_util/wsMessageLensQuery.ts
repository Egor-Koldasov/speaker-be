import { JSONSchema7 } from "json-schema";
import WsMessageBase from "../ws-message/WsMessageBase";
import LensQueryBase from "../ws-message/message/RequestToServer/LensQuery/LensQueryBase";
import { SchemaObjectOpts, schemaObject } from "./schemaObject";
import { wsMessage } from "./wsMessage";
import { lensQueryNames } from "../ws-message/message/RequestToServer/LensQuery/LensQueryName";

type WsMessageBaseJSchema = typeof WsMessageBase;
type LensQueryBaseJSchema = typeof LensQueryBase;
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

type LensQueryDataBase = NonNullable<
  WsMessageJSchemaProps["data"]["properties"]
> & {
  queryName: {
    const: (typeof lensQueryNames)[number];
  };
  queryParams?: {
    type: ["object"];
    properties?: JSONSchema7["properties"];
  };
};

export const wsMessageLensQuery = <
  LensQueryData extends LensQueryDataBase,
  Opts extends SchemaObjectOpts & { relPathToWsMessage: string } & {
    response?: boolean;
  },
>(
  lensQueryData: LensQueryData,
  opts: Opts
): LensQueryBaseJSchema => {
  const msgSchema = wsMessage(
    {
      name: {
        const: "LensQuery",
      },
      data: schemaObject({
        queryParams: {
          type: ["object"],
        },
        ...lensQueryData,
      }),
      responseForId: !opts.response ? undefined : { type: "string" },
    },
    opts
  );
  return msgSchema;
};
