import z from 'zod/v3'

export enum ChatMode {
  FreeChat = 'FreeChat',
  WordTrainingMode = 'WordTrainingMode',
}

export enum Action {
  StartWordTrainingMode = 'StartWordTrainingMode',
}

const availableActionsConfig: Record<ChatMode, Action[]> = {
  [ChatMode.FreeChat]: [Action.StartWordTrainingMode],
  [ChatMode.WordTrainingMode]: [],
}

export const chatModeSchema = z.nativeEnum(ChatMode)

export const actionChatInputMessageSchema = z.object({
  type: z.literal('action'),
})

export const messageChatInputMessageSchema = z.object({
  type: z.literal('action'),
})

export const chatInputMessageSchema = z.union([
  actionChatInputMessageSchema,
  messageChatInputMessageSchema,
])

export const chatOutputMessageSchema = z.object({})

const testMessage = {
  mode: ChatMode.FreeChat,
  availableActions: availableActionsConfig[ChatMode.FreeChat],
  type: 'action',
  action: Action.StartWordTrainingMode,
}
