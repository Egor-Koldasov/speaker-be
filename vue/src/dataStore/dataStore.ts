import { defineStore } from 'pinia'
import type { MessageName } from '../types/MessageName'
import type { MessageOutputByName } from '../types/MessageOutputByName'
import type { MessageInputByName } from '../types/MessageInputByName'
import { speakerUrl } from '../util/useSpeakerHealth'
import type { ChatCompletion } from 'openai/resources/index.mjs'

type DataStateItem<Data, Name extends string> = {
  name: Name
  data: Data | null
  loading: boolean
  errors: string[]
}

const initDateStateItem = <Data, Name extends MessageName>(
  name: Name,
): DataStateItem<Data, Name> => ({
  name,
  data: null,
  loading: false,
  errors: [],
})

const initMessageDataItem = <Name extends MessageName>(name: Name) =>
  initDateStateItem<MessageOutputByName<Name>, Name>(name)

export const useDataStore = defineStore('dataStore', {
  state: () => ({
    parseText: initMessageDataItem('parseText'),
    defineWord: initMessageDataItem('defineWord'),
    parseTextToForeign: initMessageDataItem('parseTextToForeign'),
  }),
  actions: {
    async sendMessage<Name extends MessageName>(
      input: MessageInputByName<Name>,
    ) {
      this[input.name].loading = true
      try {
        const res = await fetch(`${speakerUrl}/message`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(input),
        })
        const data = (await res.json()) as ChatCompletion.Choice
        const response = JSON.parse(
          data.message.content ?? 'null',
        ) as MessageOutputByName<Name>
        this[input.name].data = response
      } catch (err) {
        console.error(err)
        this[input.name].errors = [String(err)]
      }
      this[input.name].loading = false
    },
  },
})
