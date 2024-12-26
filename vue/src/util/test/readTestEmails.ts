// https://github.com/mailhog/MailHog/blob/master/docs/APIv2/swagger-2.0.yaml

import type { EmailData } from './EmailData'

export const readTestEmailsTo = async (to: string) => {
  const response = await fetch(
    `http://localhost:8025/api/v2/search?${new URLSearchParams({
      kind: 'to',
      query: to,
    })}`,
  )
  if (!response.ok) {
    throw new Error('Failed to fetch test emails')
  }
  const responseData = await response.json()
  return responseData as {
    count: number
    items: EmailData[]
  }
}
