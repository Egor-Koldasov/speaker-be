<script lang="ts" setup>
import { reactive, watch } from 'vue'
import { useSpeakerHealth, speakerUrl } from '../util/useSpeakerHealth'
import { useToasts } from '../uiStore/useToasts'
import type { ChatCompletion } from 'openai/resources/index.mjs'
import type { MessageParseText } from '../schema/MessageUnion.schema'

const { healthData, checkHealth } = useSpeakerHealth()
const uisToasts = useToasts()
const form = reactive({
  phrase: '',
})
const parts = reactive({
  data: [] as string[],
  loading: false,
})

const handleSubmit = async () => {
  parts.loading = true
  const message: MessageParseText = {
    name: 'parseText',
    data: {
      text: form.phrase,
    },
  }
  try {
    const res = await fetch(`${speakerUrl}/message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(message),
    })
    const data = (await res.json()) as ChatCompletion.Choice
    const response = JSON.parse(data.message.content ?? 'null') as { parts: string[] }
    parts.data = response.parts
  } catch (err) {
    console.error(err)
    return
  }

  parts.loading = false
}
watch(healthData, (newVal) => {
  console.log(newVal)
  const messageContent = newVal.data?.message.message.content
  uisToasts.addToast({
    message: `Health status: ${messageContent}`,
  })
})
</script>

<template>
  <main>
    <div
      class="health-status"
      :class="{ loading: healthData.loading, healthy: !!healthData.data }"
      @click="checkHealth"
    ></div>
    <form class="speaker-form" @submit.prevent="handleSubmit">
      <div class="parts">
        <div v-for="part in parts.data" :key="part">{{ part }}</div>
      </div>
      <textarea type="text" placeholder="Enter a phrase" v-model="form.phrase" />
      <button type="submit" class="submit-btn" :disabled="parts.loading">Learn</button>
      <progress v-if="parts.loading" />
    </form>
  </main>
</template>

<style lang="scss" scoped>
main {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.health-status {
  position: absolute;
  top: 1rem;
  left: 1rem;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #ccc;

  &.loading {
    background-color: #156a97;
    animation: pulse 0.3s infinite;
  }

  &.healthy {
    background-color: green;
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.speaker-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
  width: 100%;
  max-width: 1000px;
  max-height: 500px;

  textarea {
    width: 100%;
    height: 100%;
    resize: none;
  }

  .submit-btn {
    padding: 1rem;
  }
}

.parts {
  display: flex;
  gap: 1rem;
}
</style>
