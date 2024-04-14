import { defineStore } from 'pinia'
import type { MessageName } from '../types/MessageName'
import type { MessageOutputByName } from '../types/MessageOutputByName'
import type { MessageInputByName } from '../types/MessageInputByName'
import { speakerUrl } from '../util/useSpeakerHealth'

type DataStateItem<Data, Name extends string> = {
  name: Name
  data: Data | null
  loading: boolean
  errors: string[]
}

const initDateStateItem = <const Data, const Name extends MessageName>(
  name: Name,
): DataStateItem<Data, Name> => ({
  name,
  data: null,
  loading: false,
  errors: [],
})

const initMessageDataItem = <const Name extends MessageName>(name: Name) =>
  initDateStateItem<MessageOutputByName<Name>, Name>(name)

export const useDataStore = defineStore('dataStore', {
  state: () => ({
    parseText: initMessageDataItem('parseText'),
    defineWord: initMessageDataItem('defineWord'),
    parseTextToForeign: initMessageDataItem('parseTextToForeign'),
    textToSpeech: initDateStateItem<
      MessageOutputByName<'textToSpeech'>,
      'textToSpeech'
    >('textToSpeech'),
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
        const data = (await res.json()) as MessageOutputByName<Name>
        this[input.name].data = data
      } catch (err) {
        console.error(err)
        this[input.name].errors = [String(err)]
      }
      this[input.name].loading = false
    },
  },
})
