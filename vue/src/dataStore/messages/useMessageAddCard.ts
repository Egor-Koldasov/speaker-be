import type { Card } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { useMessage, type MessageInputParams } from '../messageStore'

export const useMessageAddCard = (reactiveProps: { card: Card }) => {
  const reactiveParams: { inputParams: MessageInputParams<'AddCard'> } = {
    inputParams: {
      name: 'AddCard',
      data: {
        card: reactiveProps.card,
        deckId: '',
      },
    },
  }
  const message = useMessage<'AddCard'>(reactiveParams)

  return message
}
