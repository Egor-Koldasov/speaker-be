<script lang="ts" setup>
import { computed, reactive, watch } from 'vue'
import { useSpeakerHealth, speakerUrl } from '../util/useSpeakerHealth'
import { useToasts } from '../uiStore/useToasts'
import type { ChatCompletion } from 'openai/resources/index.mjs'
import type { MessageParseText } from '../schema/MessageUnion.schema'
import Modal from '../components/Modal.vue'
import DefinitionItem from '../components/DefinitionItem/DefinitionItem.vue'
import LanguageSelector from '../components/LanguageSelector.vue'
import { useSettings } from '../uiStore/useSettings'

const { healthData, checkHealth } = useSpeakerHealth()
const uisToasts = useToasts()
const form = reactive({
  phrase: '',
})
const parts = reactive({
  data: null as null | NonNullable<MessageParseText['output']>,
  loading: false,
})
const uiState = reactive({
  selectedWordIndex: -1,
})
const uisSettings = useSettings()

const handleSubmit = async () => {
  parts.loading = true
  const message: MessageParseText['input'] = {
    name: 'parseText',
    data: {
      text: form.phrase,
      originalLanguages: uisSettings.originalLanguages,
      translationLanguage: uisSettings.translationLanguage ?? 'en',
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
    const response = JSON.parse(data.message.content ?? 'null') as NonNullable<
      MessageParseText['output']
    >
    parts.data = response
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
  return parts.data?.definitionParts[uiState.selectedWordIndex]
})
</script>

<template>
  <main>
    <header>
      <div class="language-bar">
        <LanguageSelector
          :language-bcp47-list="uisSettings.originalLanguages"
          @add-language-bcp47="
            (code) => uisSettings.originalLanguages.push(code.toLowerCase())
          "
          @remove-language-bcp47="
            (code) =>
              uisSettings.originalLanguages.splice(
                uisSettings.originalLanguages.indexOf(code),
                1,
              )
          "
        />
      </div>
    </header>
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
      <DefinitionItem :word="selectedWord.text" />
    </Modal>
    <form class="speaker-form" @submit.prevent="handleSubmit">
      <div class="parts">
        <button
          type="button"
          class="part"
          :class="{ selected: uiState.selectedWordIndex === index }"
          @click="uiState.selectedWordIndex = index"
          v-for="(part, index) in parts.data?.definitionParts ?? []"
          :key="part.text"
        >
          <div class="part-text">
            <!-- {{ part.languageOriginal }} -->
            {{ part.text }}
          </div>
          <div class="part-translation">
            <!-- {{ part.languageTranslated }} -->
            {{ part.translation }}
          </div>
        </button>
      </div>
      <div v-if="parts.data?.translation">
        {{ parts.data.translation.text }}
      </div>
      <textarea
        type="text"
        placeholder="Enter a phrase"
        v-model="form.phrase"
        @keydown.meta.enter="handleSubmit"
      />
      <button type="submit" class="submit-btn" :disabled="parts.loading">
        Learn
      </button>
      <progress v-if="parts.loading" />
    </form>
  </main>
</template>

<style lang="scss" scoped>
main {
  position: fixed;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  header {
    margin-bottom: auto;
    width: 100%;
    display: flex;
    padding: 0.5rem;
    .language-bar {
      margin-left: auto;
      .dropdown {
        margin: 0;
      }
    }
  }
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
    display: flex;
    flex-direction: column;
    border: 1px solid #89147f;
    border-radius: 0.5rem;
    cursor: pointer;
    background-color: transparent;
    padding: 0;
    .part-text {
      border-bottom: 1px solid #89147f;
      width: 100%;
      padding: 0 1rem;
    }
    .part-translation {
      padding: 0 1rem;
    }

    &:hover {
      background-color: #89147f;
    }

    &.selected {
      background-color: #148954;
    }
  }
}
</style>
