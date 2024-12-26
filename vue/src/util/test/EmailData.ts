export type EmailData = {
  ID: string
  From: {
    Relays: null | string
    Mailbox: string
    Domain: string
    Params: string
  }
  To: Array<{
    Relays: null | string
    Mailbox: string
    Domain: string
    Params: string
  }>
  Content: {
    Headers: {
      'Content-Transfer-Encoding': string[]
      'Content-Type': string[]
      Date: string[]
      From: string[]
      'Message-ID': string[]
      'Mime-Version': string[]
      Received: string[]
      'Return-Path': string[]
      Subject: string[]
      To: string[]
    }
    Body: string
    Size: number
    MIME: null | string
  }
  Created: string
  MIME: null | string
  Raw: {
    From: string
    To: string[]
    Data: string
    Helo: string
  }
}
