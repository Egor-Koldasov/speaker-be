<script setup lang="ts">
import { onMounted, reactive, watch } from 'vue'
import { speakerUrl } from '../../util/useSpeakerHealth'
import type { ChatCompletion } from 'openai/resources/index.mjs'
import type { Word } from '../../schema/Main.schema'
import tags from 'language-tags'
import type { MessageDefineWord } from '../../schema/Main.schema'
import { useSettings } from '../../uiStore/useSettings'

// # Props, State
const props = defineProps<{
  word: string
}>()

const definitionData = reactive({
  data: null as null | { word: Word },
  loading: false,
})

const uisSettings = useSettings()
// # Hooks
// # Computed
// # Callbacks
const loadDefinition = async () => {
  definitionData.loading = true
  const message: MessageDefineWord['input'] = {
    name: 'defineWord',
    data: {
      wordString: props.word,
      context: props.word,
      originalLanguages: uisSettings.originalLanguages,
      translationLanguage: uisSettings.translationLanguage || 'en',
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
      MessageDefineWord['output']
    >
    definitionData.data = { word: response.definition }
  } catch (err) {
    console.error(err)
  }

  definitionData.loading = false
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
    <div v-if="definitionData.loading">Loading...</div>
    <div v-else-if="definitionData.data">
      <ul>
        <li>
          <label>Language original</label>
          <textarea
            rows="1"
            :value="
              tags
                .language(definitionData.data.word.languageOriginal)
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
            v-model="definitionData.data.word.originalWord"
            readonly
          />
        </li>
        <li>
          <label>Translation</label>
          <textarea
            rows="1"
            v-model="definitionData.data.word.translation"
            readonly
          />
        </li>
        <li>
          <label>Neutral form</label>
          <textarea
            rows="1"
            v-model="definitionData.data.word.neutralForm"
            readonly
          />
        </li>
        <li>
          <label>Synonyms</label>
          <textarea
            rows="1"
            v-model="definitionData.data.word.synonyms"
            readonly
          />
        </li>
        <li>
          <label>Definition translated</label>
          <textarea
            rows="1"
            v-model="definitionData.data.word.definitionTranslated"
            readonly
          />
        </li>
        <li>
          <label>Definition original</label>
          <textarea
            rows="1"
            v-model="definitionData.data.word.definitionOriginal"
            readonly
          />
        </li>
        <li>
          <label>Origin</label>
          <textarea
            rows="1"
            v-model="definitionData.data.word.origin"
            readonly
          />
        </li>
        <li>
          <label>Examples</label>
          <ul>
            <li
              v-for="example in definitionData.data.word.examples"
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
