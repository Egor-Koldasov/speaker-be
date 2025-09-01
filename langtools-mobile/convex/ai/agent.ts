import { openai } from '@ai-sdk/openai'
import { Agent } from '@convex-dev/agent'
import { components } from '../_generated/api'

const gpt5Mini = openai.chat('gpt-5-mini')

export const agent = new Agent(components.agent, {
  name: 'Chat',
  languageModel: gpt5Mini,
})
