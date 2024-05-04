<script lang="ts" setup>
import { computed, reactive, watch } from 'vue'
import { useSpeakerHealth } from '../../util/useSpeakerHealth'
import { useToasts } from '../../uiStore/useToasts'
import DefinitionItem from '../DefinitionItem/DefinitionItem.vue'
import LanguageSelector from '../LanguageSelector.vue'
import { useSettings } from '../../uiStore/useSettings'
import {
  useMessageStore,
  type MessageInputParams,
} from '../../dataStore/messageStore'
import Page from '../layout/Page.vue'
import PageHeader from '../layout/PageHeader.vue'
import LanguageBar from '../LanguageBar.vue'
import { useMessage } from '../../dataStore/messageStore'

const { healthData, checkHealth } = useSpeakerHealth()
const uisToasts = useToasts()

const uiState = reactive({
  selectedWordIndex: -1,
})
const uisSettings = useSettings()
const form = reactive({
  phrase: '',
  messageParams: {
    inputParams: {
      name: 'ParseTextFromForeign',
      data: {
        text: '',
        originalLanguages: uisSettings.originalLanguages,
        translationLanguage: uisSettings.translationLanguage ?? 'en',
      },
    } satisfies MessageInputParams<'ParseTextFromForeign'>,
  },
})
const messageStore = useMessageStore()

const messageQuery = useMessage(form.messageParams)
const messageResult = computed(
  () => messageQuery.value.data?.output?.data ?? null,
)

const handleSubmit = async () => {
  form.messageParams.inputParams.data.text = form.phrase
  form.messageParams.inputParams.data.originalLanguages =
    uisSettings.originalLanguages
  form.messageParams.inputParams.data.translationLanguage =
    uisSettings.translationLanguage ?? 'en'
  messageStore.sendMessage(form.messageParams.inputParams)
}
watch(healthData, (newVal) => {
  console.log(newVal)
  const messageContent = newVal.data?.message.message.content
  uisToasts.addToast({
    message: `Health status: ${messageContent}`,
  })
})

const selectedWord = computed(() => {
  return messageResult.value?.definitionParts[uiState.selectedWordIndex]
})
</script>

<template>
  <Page>
    <PageHeader>
      <LanguageBar>
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
        <LanguageSelector
          :language-bcp47-list="[uisSettings.translationLanguage || 'en']"
          @add-language-bcp47="
            (code) => (uisSettings.translationLanguage = code.toLowerCase())
          "
          @remove-language-bcp47="(code) => {}"
        />
      </LanguageBar>
    </PageHeader>
    <div
      class="health-status"
      :class="{ loading: healthData.loading, healthy: !!healthData.data }"
      @click="checkHealth"
    ></div>
    <div class="col2">
      <form class="speaker-form" @submit.prevent="handleSubmit">
        <div class="parts">
          <button
            type="button"
            class="part"
            :class="{ selected: uiState.selectedWordIndex === index }"
            @click="uiState.selectedWordIndex = index"
            v-for="(part, index) in messageResult?.definitionParts ?? []"
            :key="index"
            :data-index="index"
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
        <div v-if="messageResult?.translation">
          {{ messageResult.translation.text }}
        </div>
        <textarea
          type="text"
          placeholder="Enter a phrase"
          v-model="form.phrase"
          @keydown.meta.enter="handleSubmit"
        />
        <button
          type="submit"
          class="submit-btn"
          :disabled="messageQuery.refreshing"
        >
          Learn
        </button>
        <progress v-if="messageQuery.refreshing" />
      </form>
      <DefinitionItem
        v-if="!!selectedWord"
        :word="selectedWord.text"
        :context="form.phrase"
      />
    </div>
  </Page>
</template>

<style lang="scss" scoped>
.health-status {
  display: none;
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
  overflow-x: auto;
  flex-grow: 1;
  flex-shrink: 0;

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
      text-wrap: nowrap;
    }
    .part-translation {
      padding: 0 1rem;
      text-wrap: nowrap;
    }

    &:hover {
      background-color: #89147f;
    }

    &.selected {
      background-color: #148954;
    }
  }
}
.col2 {
  display: flex;
  width: 100%;
  height: 100%;
  justify-content: space-around;
}
</style>
