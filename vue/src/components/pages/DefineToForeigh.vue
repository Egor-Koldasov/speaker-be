<script setup lang="ts">
import { reactive } from 'vue'
import { useSettings } from '../../uiStore/useSettings'
import LanguageBar from '../LanguageBar.vue'
import LanguageSelector from '../LanguageSelector.vue'
import Page from '../layout/Page.vue'
import PageHeader from '../layout/PageHeader.vue'
import { useDataStore } from '../../dataStore/dataStore'

// # Props, State
const form = reactive({
  text: '',
})
const uiState = reactive({
  selectedWordIndex: -1,
})
// # Hooks
const uisSettings = useSettings()
const dataStore = useDataStore()
// # Computed
// # Callbacks
const handleSubmit = async () => {
  dataStore.sendMessage({
    name: 'parseTextToForeign',
    data: {
      text: form.text,
      nativeLanguages: uisSettings.nativeLanguages,
      primaryForeignLanguage: uisSettings.primaryForeignLanguage,
    },
  })
}
// # Watchers
</script>
<template>
  <Page class="DefineToForeigh">
    <PageHeader>
      <LanguageBar>
        <LanguageSelector
          :language-bcp47-list="uisSettings.nativeLanguages"
          @add-language-bcp47="
            (code) => uisSettings.nativeLanguages.push(code.toLowerCase())
          "
          @remove-language-bcp47="
            (code) =>
              uisSettings.nativeLanguages.splice(
                uisSettings.nativeLanguages.indexOf(code),
                1,
              )
          "
        />
        <LanguageSelector
          :language-bcp47-list="[uisSettings.primaryForeignLanguage]"
          @add-language-bcp47="
            (code) => (uisSettings.primaryForeignLanguage = code.toLowerCase())
          "
          @remove-language-bcp47="(code) => {}"
        />
      </LanguageBar>
    </PageHeader>
    <div class="col2">
      <form @submit.prevent="handleSubmit">
        <div class="parts">
          <button
            type="button"
            class="part"
            :class="{ selected: uiState.selectedWordIndex === index }"
            @click="uiState.selectedWordIndex = index"
            v-for="(part, index) in dataStore.parseTextToForeign.data
              ?.translationChoices[0]?.definitionParts ?? []"
            :key="part.text"
          >
            <div class="part-text">
              <!-- {{ part.languageOriginal }} -->
              {{ part.text }}
            </div>
            <div class="part-translation">
              <!-- {{ part.languageTranslated }} -->
              {{ part.translationToNative }}
            </div>
          </button>
        </div>
        <div v-if="dataStore.ParseTextFromForeign.data?.translation">
          {{
            dataStore.parseTextToForeign.data?.translationChoices[0]
              ?.translation.text
          }}
        </div>
        <textarea
          type="text"
          placeholder="Enter a phrase"
          v-model="form.text"
          @keydown.meta.enter="handleSubmit"
        />
        <button
          type="submit"
          class="submit-btn"
          :disabled="dataStore.parseTextToForeign.loading"
        >
          Translate
        </button>
        <progress v-if="dataStore.parseTextToForeign.loading" />
      </form>
    </div>
  </Page>
</template>
<style scoped lang="scss">
.DefineToForeigh {
  .col2 {
    display: flex;
    width: 100%;
    height: 100%;
    justify-content: space-around;
  }
  form {
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
}
.parts {
  display: flex;
  gap: 1rem;
  overflow-x: auto;

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
