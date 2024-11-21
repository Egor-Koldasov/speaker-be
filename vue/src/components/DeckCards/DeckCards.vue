<script setup lang="ts">
import { useMessage } from '../../dataStore/messageStore'
import type { Deck } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { reactive } from 'vue'

// # Props, State
const props = defineProps<{
  deck: Deck
}>()
const reactiveParams = reactive({
  inputParams: {
    name: 'GetCards' as const,
    data: {
      deckId: props.deck.id,
    },
  },
})
// # Hooks
const cardsMessage = useMessage<'GetCards'>(reactiveParams, {
  runOnMount: true,
  runOnUpdate: true,
})
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <div class="DeckCards">
    <div class="card-list" v-if="cardsMessage.data?.output?.data">
      <div
        class="card-item"
        v-for="card in cardsMessage.data?.output?.data.cards"
        :key="card.id"
      >
        {{ card.definition.originalWord }}
      </div>
    </div>
  </div>
</template>
<style scoped lang="scss">
.DeckCards {
}

.card-item {
  &::before {
    content: '•';
    margin-right: 0.5em;
  }
}
</style>
