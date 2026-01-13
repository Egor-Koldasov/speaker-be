import { openai } from '@ai-sdk/openai'
import { Agent } from '@convex-dev/agent'
import { components } from '../_generated/api'
import { suggestNewWordsTool } from './suggestNewWordsTool'

const gpt5Mini = openai.chat('gpt-5-mini')
const gpt5 = openai.chat('gpt-5.2')

const opts = {
  languageModel: gpt5Mini,
}

export const agent = new Agent(components.agent, {
  name: 'Chat',
  ...opts,
})

export const chatAgent = new Agent(components.agent, {
  name: 'Chat Assistant',
  ...opts,
  languageModel: gpt5,
  tools: {
    suggestNewWordsTool,
  },
})
