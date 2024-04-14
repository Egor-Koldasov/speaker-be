<script setup lang="ts">
import tags from 'language-tags'
import { onMounted, watch } from 'vue'
import { useDataStore } from '../../dataStore/dataStore'
import { useSettings } from '../../uiStore/useSettings'

// # Props, State
const props = defineProps<{
  word: string
  context: string
}>()

// # Hooks
const uisSettings = useSettings()
const dataStore = useDataStore()
// # Computed
// # Callbacks
const loadDefinition = async () => {
  dataStore.sendMessage({
    name: 'defineWord',
    data: {
      wordString: props.word,
      context: props.context,
      originalLanguages: uisSettings.originalLanguages,
      translationLanguage: uisSettings.translationLanguage || 'en',
    },
  })
}
// # Watchers
onMounted(() => {
  loadDefinition()
})
watch(
  () => props.word,
  () => {
    loadDefinition()
  },
)
</script>
<template>
  <div class="DefinitionItem">
    <div v-if="dataStore.defineWord.loading">Loading...</div>
    <div v-else-if="dataStore.defineWord.data">
      <ul>
        <li>
          <label>Language original</label>
          <textarea
            rows="1"
            :value="
              tags
                .language(dataStore.defineWord.data.definition.languageOriginal)
                ?.descriptions()
                .join(', ')
            "
            readonly
          />
        </li>
        <li>
          <label>Original word</label>
          <textarea
            rows="1"
            v-model="dataStore.defineWord.data.definition.originalWord"
            readonly
          />
        </li>
        <li>
          <label>Translation</label>
          <textarea
            rows="1"
            v-model="dataStore.defineWord.data.definition.translation"
            readonly
          />
        </li>
        <li>
          <label>Neutral form</label>
          <textarea
            rows="1"
            v-model="dataStore.defineWord.data.definition.neutralForm"
            readonly
          />
        </li>
        <li>
          <label>Synonyms</label>
          <textarea
            rows="1"
            v-model="dataStore.defineWord.data.definition.synonyms"
            readonly
          />
        </li>
        <li>
          <label>Definition translated</label>
          <textarea
            rows="1"
            v-model="dataStore.defineWord.data.definition.definitionTranslated"
            readonly
          />
        </li>
        <li>
          <label>Definition original</label>
          <textarea
            rows="1"
            v-model="dataStore.defineWord.data.definition.definitionOriginal"
            readonly
          />
        </li>
        <li>
          <label>Origin</label>
          <textarea
            rows="1"
            v-model="dataStore.defineWord.data.definition.origin"
            readonly
          />
        </li>
        <li>
          <label>Examples</label>
          <ul>
            <li
              v-for="example in dataStore.defineWord.data.definition.examples"
              :key="example.original"
            >
              <textarea rows="1" v-model="example.original" readonly />
              <textarea rows="1" v-model="example.translation" readonly />
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div v-else>No definition found for "{{ word }}"</div>
  </div>
</template>
<style scoped lang="scss">
.DefinitionItem {
  width: 70vw;
  max-width: 1000px;
  max-height: 90vh;
  overflow: auto;
  flex-shrink: 1;
  ul {
    li {
      list-style-type: none;
      label {
        font-size: 1rem;
      }
      textarea {
        padding: 0 0.5rem;
        height: auto;
        background: transparent;
        border: none;
        border-bottom: 1px solid #483848;

        &:focus {
          outline: none;
          box-shadow: none;
          border-bottom: 1px solid #9435a4;
        }
      }
    }
  }
}
</style>
