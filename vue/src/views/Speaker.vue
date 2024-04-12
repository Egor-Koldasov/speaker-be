<script lang="ts" setup>
import { computed, reactive, watch } from 'vue'
import { useSpeakerHealth, speakerUrl } from '../util/useSpeakerHealth'
import { useToasts } from '../uiStore/useToasts'
import type { ChatCompletion } from 'openai/resources/index.mjs'
import type { MessageParseText } from '../schema/MessageUnion.schema'
import Modal from '../components/Modal.vue'
import DefinitionItem from '../components/DefinitionItem/DefinitionItem.vue'

const { healthData, checkHealth } = useSpeakerHealth()
const uisToasts = useToasts()
const form = reactive({
  phrase: '',
})
const parts = reactive({
  data: [] as string[],
  loading: false,
})
const uiState = reactive({
  selectedWordIndex: -1,
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

const selectedWord = computed(() => {
  return parts.data[uiState.selectedWordIndex]
})
</script>

<template>
  <main>
    <div
      class="health-status"
      :class="{ loading: healthData.loading, healthy: !!healthData.data }"
      @click="checkHealth"
    ></div>
    <Modal
      v-if="!!selectedWord"
      @close="uiState.selectedWordIndex = -1"
      :title="`Define ${selectedWord}`"
    >
      <DefinitionItem :word="selectedWord" />
    </Modal>
    <form class="speaker-form" @submit.prevent="handleSubmit">
      <div class="parts">
        <button
          type="button"
          v-for="(part, index) in parts.data"
          :key="part"
          class="part"
          :class="{ selected: uiState.selectedWordIndex === index }"
          @click="uiState.selectedWordIndex = index"
        >
          {{ part }}
        </button>
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

  .part {
    padding: 0 1rem;
    border: 1px solid #89147f;
    border-radius: 0.5rem;
    cursor: pointer;
    background-color: transparent;

    &:hover {
      background-color: #89147f;
    }

    &.selected {
      background-color: #148954;
    }
  }
}
</style>
