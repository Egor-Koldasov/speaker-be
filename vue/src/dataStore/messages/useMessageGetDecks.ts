import { useMessage } from '../messageStore'

export const useMessageGetDecks = () => {
  const message = useMessage<'GetDecks'>(
    {
      inputParams: {
        name: 'GetDecks',
        data: {},
      },
    },
    {
      runOnMount: true,
    },
  )
  return message
}
