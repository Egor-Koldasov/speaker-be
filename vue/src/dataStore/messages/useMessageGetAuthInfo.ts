import { useMessage } from '../messageStore'

export const useMessageGetAuthInfo = () => {
  const message = useMessage<'GetAuthInfo'>(
    {
      inputParams: {
        name: 'GetAuthInfo',
        data: {},
      },
    },
    {
      runOnMount: true,
    },
  )
  return message
}
