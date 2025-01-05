<script setup lang="ts">
import { computed, effect, reactive, watch } from 'vue'
import { useCreateCardConfig } from '../../planning/Action/useCreateCardConfig'
import { makeDbModelBase } from '../../util/model-factories/makeDbModelBase'
import CardConfigSelector from '../CardConfigSelector.vue'
import Page from '../layout/Page.vue'
import Button from '../ui/Button.vue'
import { useToasts } from '../../uiStore/useToasts'
import { useCardConfigSelector } from '../../uiStore/useCardConfigSelector'
import { useLensQueryCardConfig } from '../../planning/Lens/useLensQueryCardConfig'
import LabelBox from '../ui/LabelBox.vue'
import TextField from '../ui/TextField.vue'
import LabelText from '../ui/LabelText.vue'
import type { CardConfig } from 'speaker-json-schema/gen-schema-ts/Main.schema'

// # Props, State
const form = reactive({
  cardConfig: null as null | Pick<CardConfig, 'name'>,
})
// # Hooks
const actionCreateCardConfig = useCreateCardConfig()
const toasts = useToasts()
const cardConfigSelector = useCardConfigSelector()
const lensQueryCardConfig = useLensQueryCardConfig()
// # Computed
const cardConfig = computed(() => lensQueryCardConfig.$state.memData.cardConfig)
// # Callbacks
const createCardConfig = () => {
  actionCreateCardConfig.$state.memActionParams.cardConfig = {
    ...makeDbModelBase({ name: 'CardConfig' }),
    name: `Unnamed card config ${new Date()}`,
    userId: '',
  }
  actionCreateCardConfig.requestMainDb()
}
// # Watchers
watch(
  () => [actionCreateCardConfig.lastFetchedMainAt],
  () => {
    if (!actionCreateCardConfig.$state.lastFetchedMainAt) {
      toasts.addToast({ message: 'Created card config' })
    }
  },
)
effect(() => {
  lensQueryCardConfig.$state.memDataArgs.cardConfigId =
    cardConfigSelector.$state.selectedCardConfigId
})
effect(() => {
  form.cardConfig = cardConfig.value ?? null
})
</script>
<template>
  <Page>
    <div class="CardCreator">
      <div class="card-list-manager">
        <CardConfigSelector />
        <Button class="secondary" @click="createCardConfig">
          <div class="font-icon">+</div>
        </Button>
      </div>
      <div class="CardConfig" v-if="form.cardConfig">
        <LabelBox>
          <LabelText>Name</LabelText>
          <TextField v-model="form.cardConfig.name" />
        </LabelBox>
      </div>
    </div>
  </Page>
</template>
<style scoped lang="scss">
.CardCreator {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.card-list-manager {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ffffff33;
  .CardConfigSelector::v-deep {
    flex-grow: 1;
  }
}
.font-icon {
  font-size: 2rem;
  font-weight: 400;
  display: flex;
  align-items: center;
}
.CardConfig {
  .LabelBox::v-deep {
    flex-grow: 1;
  }
  .TextField::v-deep {
    flex-grow: 1;
  }
}
</style>
