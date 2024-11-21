<script setup lang="ts">
import Page from '../layout/Page.vue'
import PageHeader from '../layout/PageHeader.vue'
import DeckCards from '../DeckCards/DeckCards.vue'
import { useMessage } from '../../dataStore/messageStore'

// # Props, State
// # Hooks
const decksMessage = useMessage<'GetDecks'>(
  {
    inputParams: {
      name: 'GetDecks',
      data: {},
    },
  },
  {
    runOnMount: true,
  },
)
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <Page>
    <PageHeader />
    <div class="Decks">
      <div class="deck-list" v-if="decksMessage.data?.output?.data">
        <div
          class="deck-item"
          v-for="deck in decksMessage.data.output.data.decks"
          :key="deck.id"
        >
          <div class="deck-name">{{ deck.name }}</div>
          <DeckCards :deck="deck" />
        </div>
      </div>
    </div>
  </Page>
</template>
<style scoped lang="scss">
.Decks {
  height: 1px;
  flex-grow: 1;
}
</style>
