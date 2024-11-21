<script setup lang="ts">
import tags from 'language-tags'
import { computed, reactive, watch, type Ref } from 'vue'
import { useMessage, useMessageStore } from '../../dataStore/messageStore'
import { useMessageGetDecks } from '../../dataStore/messages/useMessageGetDecks'
import { useMessageAddCard } from '../../dataStore/messages/useMessageAddCard'
import { useSettings } from '../../uiStore/useSettings'
import type { Definition } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { uuidv7 } from 'uuidv7'

// # Props, State
const props = defineProps<{
  word: Ref<string>
  context: Ref<string>
}>()

// # Hooks
const uisSettings = useSettings()
const form = reactive({
  inputParams: {
    name: 'DefineTerm' as const,
    data: {
      term: props.word.value,
      context: props.context.value,
      originalLanguages: uisSettings.originalLanguages,
      translationLanguage: uisSettings.translationLanguage || 'en',
    },
  },
})
const message = useMessage<'DefineTerm'>(form, {
  runOnMount: true,
  runOnUpdate: true,
})
const messageStore = useMessageStore()

// const messageAddCard = useMessageAddCard()

const messageDecks = useMessageGetDecks()
// # Computed
const messageData = computed(() => message.value.data?.output?.data)
// # Callbacks
const addCard = (definition: Definition) => {
  messageStore.sendMessage({
    name: 'AddCard',
    data: {
      deckId: '',
      card: {
        id: uuidv7(),
        definition,
      },
    },
  })
}

// # Watchers

watch([props.word, props.context], () => {
  form.inputParams.data.term = props.word.value
  form.inputParams.data.context = props.context.value
})
</script>
<template>
  <div class="DefinitionItem">
    <div v-if="message.refreshing">Loading...</div>
    <div v-else-if="messageData" class="message-data">
      <div class="button-bar">
        <button
          @click="
            () => messageData?.definition && addCard(messageData.definition)
          "
        >
          Add
        </button>
      </div>
      <div class="decks" v-if="messageDecks.data?.output?.data">
        <label>Decks</label>
        <ul>
          <li
            v-for="deck in messageDecks.data.output.data.decks"
            :key="deck.id"
            class="deck"
          >
            <input
              type="checkbox"
              :id="deck.id"
              class="deck-input"
              :checked="
                !!messageData.decks.find(
                  (ownerDeck) => ownerDeck.id === deck.id,
                )
              "
            />
            <label :for="deck.id" class="deck-label">{{ deck.name }}</label>
          </li>
        </ul>
      </div>
      <ul>
        <li>
          <label>Language original</label>
          <textarea
            rows="2"
            :value="
              tags
                .language(messageData.definition.languageOriginal)
                ?.descriptions()
                .join(', ')
            "
          />
        </li>
        <li>
          <label>Original word</label>
          <textarea rows="2" v-model="messageData.definition.originalWord" />
        </li>
        <li>
          <label>Translation</label>
          <textarea rows="2" v-model="messageData.definition.translation" />
        </li>
        <li>
          <label>Neutral form</label>
          <textarea rows="2" v-model="messageData.definition.neutralForm" />
        </li>
        <li>
          <label>Synonyms</label>
          <textarea rows="2" v-model="messageData.definition.synonyms" />
        </li>
        <li>
          <label>Definition translated</label>
          <textarea
            rows="2"
            v-model="messageData.definition.definitionTranslated"
          />
        </li>
        <li>
          <label>Definition original</label>
          <textarea
            rows="2"
            v-model="messageData.definition.definitionOriginal"
          />
        </li>
        <li>
          <label>Origin</label>
          <textarea rows="2" v-model="messageData.definition.origin" />
        </li>
        <li>
          <ul class="example-list">
            <li
              v-for="(example, index) in messageData.definition.examples"
              :key="example.original"
              class="example-item"
            >
              <label>Example #{{ index + 1 }}</label>

              <textarea rows="2" v-model="example.original" />
              <textarea rows="2" v-model="example.translation" />
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
  width: 40vw;
  max-width: 1000px;
  max-height: 90vh;
  overflow: auto;
  flex-shrink: 0;
  background-color: #1c161e;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  ul {
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 16px;

    li {
      list-style-type: none;
      label {
        font-size: 1rem;
      }
      textarea {
        padding: 0.5rem;
        height: auto;
        background: transparent;
        border: none;
        background-color: #483848;
        border-bottom: 1px solid #483848;

        &:focus {
          outline: none;
          box-shadow: none;
          border-bottom: 1px solid #9435a4;
        }
      }
    }
  }
  .example-list {
    display: flex;
    flex-direction: column;
  }
  .example-item {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
}
.button-bar {
  display: flex;
}
.message-data {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.deck {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
</style>
