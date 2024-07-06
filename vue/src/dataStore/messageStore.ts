import { defineStore } from 'pinia'
import type { MessageName } from '../types/message/MessageName'
import type { MessageOutputByName } from '../types/message/MessageOutputByName'
import type { MessageInputByName } from '../types/message/MessageInputByName'
import { speakerUrl } from '../util/useSpeakerHealth'
import { uuidv7 } from '@kripod/uuidv7'
import type { MessageUnion } from '../types/message/MessageUnion'
import type { MessageByName } from '../types/message/MessageByName'
import { isEqual, omit } from 'lodash'
import dayjs from 'dayjs'
import { computed, effect, onMounted, toRaw } from 'vue'

type MessageState<Message extends MessageUnion> = {
  input: Message['input']
  output: Message['output'] | null
  requestedAt: string
  loading: boolean
}

type MessageGroupState<Message extends MessageUnion> = {
  messageById: Record<Message['input']['id'], MessageState<Message>>
}

const initMessageDataItem = <const Name extends MessageName>(name: Name) => {
  const messageGroupState: MessageGroupState<MessageByName<Name>> = {
    messageById: {} as any,
  }
  return { [name]: messageGroupState } as {
    [K in Name]: typeof messageGroupState
  }
}

export type MessageInputParams<Name extends MessageName> = {
  name: MessageInputByName<Name>['name']
  data: MessageInputByName<Name>['data']
}

export const useMessageStore = defineStore('messageStore', {
  state: () => ({
    ...initMessageDataItem('ParseTextFromForeign'),
    ...initMessageDataItem('DefineTerm'),
    // defineWord: initMessageDataItem('defineWord'),
    // parseTextToForeign: initMessageDataItem('parseTextToForeign'),
    // textToSpeech: initDataStateItem<
    //   MessageOutputByName<'textToSpeech'>,
    //   'textToSpeech'
    // >('textToSpeech'),
  }),
  actions: {
    async sendMessage<Name extends MessageName>(
      inputParams: MessageInputParams<Name>,
    ) {
      const input: MessageInputByName<Name> = {
        ...inputParams,
        id: uuidv7(),
      } as MessageInputByName<Name>
      const messageGroup = this[input.name]
      messageGroup.messageById[input.id] = {
        input,
        output: null,
        requestedAt: new Date().toISOString(),
        loading: true,
      } as (typeof messageGroup.messageById)[string]
      try {
        const res = await fetch(`${speakerUrl}/message`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(input),
        })
        const data = (await res.json()) as { output: MessageOutputByName<Name> }
        messageGroup.messageById[input.id].output = data.output
      } catch (err) {
        console.error(err)
        messageGroup.messageById[input.id].output = {
          id: input.id,
          // Type generator does dot generate nullable refs
          data: null as any,
          name: input.name,
          errors: [
            {
              message: String(err),
              name: 'Unknown',
            },
          ],
        }
      }
      messageGroup.messageById[input.id].loading = false
    },
  },
})

type UseMessageOpts = {
  runOnMount?: boolean
  runOnUpdate?: boolean
}
export const useMessage = <const Name extends MessageName>(
  reactiveParams: { inputParams: MessageInputParams<Name> },
  opts: UseMessageOpts = {},
) => {
  const { runOnMount = false } = opts
  const messageStore = useMessageStore()
  const messageState = computed(
    () => {
      const inputParams = reactiveParams.inputParams
      const messageGroup = messageStore[
        reactiveParams.inputParams.name
      ] as MessageGroupState<MessageByName<Name>>
      const input: MessageInputByName<Name> = {
        ...reactiveParams.inputParams,
        id: uuidv7(),
      } as MessageInputByName<Name>

      const pendingRequests: MessageState<MessageByName<Name>>[] = []
      const finishedRequests: MessageState<MessageByName<Name>>[] = []
      let lastFinishedRequest: MessageState<MessageByName<Name>> | null = null
      ;(
        Object.values(messageGroup.messageById) as MessageState<
          MessageByName<Name>
        >[]
      ).forEach((message) => {
        const isMessageSame = isEqual(
          omit(toRaw(message.input as any), 'id'),
          omit(toRaw(input as any), 'id'),
        )
        if (!isMessageSame) return
        if (message.loading) pendingRequests.push(message)
        if (message.output) {
          finishedRequests.push(message)
          if (
            !lastFinishedRequest ||
            dayjs(message.requestedAt).isAfter(
              dayjs(lastFinishedRequest.requestedAt),
            )
          ) {
            lastFinishedRequest = message
          }
        }
      })
      const refreshing = pendingRequests.length > 0
      const queryState = {
        loading: refreshing && finishedRequests.length === 0,
        refreshing,
        data: lastFinishedRequest as MessageState<MessageByName<Name>> | null,
      }
      return queryState
    },
    {
      onTrack(event) {
        console.log('onTrack', event)
      },
      onTrigger(event) {
        console.log('onTrigger', event)
      },
    },
  )
  onMounted(() => {
    if (runOnMount) {
      void messageStore.sendMessage(reactiveParams.inputParams)
    }
  })
  effect(() => {
    if (opts.runOnUpdate) {
      void messageStore.sendMessage(reactiveParams.inputParams)
    }
  })
  return messageState
}
