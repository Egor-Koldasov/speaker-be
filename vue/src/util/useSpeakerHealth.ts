import type { ChatCompletion } from 'openai/resources/index.mjs'
import { reactive } from 'vue'

type HealthData = {
  status: string
  message: ChatCompletion.Choice
}

export const speakerUrl = import.meta.env.VITE_SPEAKER_URL
if (!speakerUrl) {
  console.warn('Speaker URL not found')
}

export const useSpeakerHealth = () => {
  const healthData = reactive({ data: null as null | HealthData, loading: false })

  const checkHealth = async () => {
    healthData.loading = true
    const response = await fetch(`${speakerUrl}/health`)
    healthData.loading = false
    healthData.data = await response.json()
  }

  return { healthData, checkHealth }
}
