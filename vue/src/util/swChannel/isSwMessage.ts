export type SwMessage = { [K in string]?: unknown } & { name: unknown }

export const isSwMessage = (message: MessageEvent<unknown>): message is MessageEvent<SwMessage> =>
  !!message.data && typeof message.data === 'object' && 'name' in message.data
