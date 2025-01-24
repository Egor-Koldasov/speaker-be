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
import TextArea from '../ui/TextArea.vue'
import dayjs from 'dayjs'
import { useLensQueryUserCardConfigs } from '../../planning/Lens/useLensQueryUserCardConfigs'

// # Props, State
const form = reactive({
  cardConfig: null as null | Pick<CardConfig, 'name' | 'prompt'>,
})
// # Hooks
const toasts = useToasts()
const cardConfigSelector = useCardConfigSelector()
const lensQueryCardConfig = useLensQueryCardConfig()
const userCardConfig = useLensQueryUserCardConfigs()
const actionCreateCardConfig = useCreateCardConfig({
  onSuccess(requestParams) {
    toasts.addToast({ message: 'Card config created ' })
    cardConfigSelector.$state.selectedCardConfigId = requestParams.cardConfig.id
  },
})
// # Computed
const cardConfig = computed(() => lensQueryCardConfig.$state.memData.cardConfig)
// # Callbacks
const createCardConfig = () => {
  actionCreateCardConfig.$state.memActionParams.cardConfig = {
    ...makeDbModelBase({ name: 'CardConfig' }),
    name: `Unnamed card config ${userCardConfig.$state.memData.cardConfigs.length + 1}`,
    prompt: '',
  }
  actionCreateCardConfig.requestMainDb()
}
// # Watchers
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
        <Button class="create-card-config-button" @click="createCardConfig">
          <div class="font-icon">+</div>
        </Button>
      </div>
      <div
        class="CardConfig"
        v-if="
          form.cardConfig && lensQueryCardConfig.$state.memDataArgs.cardConfigId
        "
      >
        <LabelBox>
          <LabelText>Name</LabelText>
          <TextField v-model="form.cardConfig.name" />
        </LabelBox>
        <LabelBox :always-wrap="true">
          <LabelText>Prompt</LabelText>
          <TextArea
            v-model="form.cardConfig.prompt"
            placeholder="Enter a prompt that will be added to every field prompt when generating their values"
          />
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
  gap: 0;
  flex-wrap: wrap;
  align-items: center;
  /* padding: 0 0.4rem; */
  border-bottom: 0;
  :deep(.CardConfigSelector) {
    flex-grow: 1;
    background-color: #39293f;
    box-shadow: 0 3px 0px 0px #231927;
    border-top-left-radius: 0.4rem;
    border-bottom-left-radius: 0.4rem;
  }
  :deep(.Select) {
    background-color: transparent;
  }
  .create-card-config-button {
    border-left: 1px solid #ffffff22;
    border-radius: 0;
    background-color: #39293f;
    box-shadow: 0 3px 0px 0px #231927;
    border-top-right-radius: 0.4rem;
    border-bottom-right-radius: 0.4rem;
    transition: 0s;
    &:active {
      box-shadow: none;
      transform: translateY(3px);
      border-left-color: transparent;
    }
  }
}
.font-icon {
  font-size: 1.5rem;
  font-weight: 400;
  display: flex;
  align-items: center;
}
.CardConfig {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  :deep(.LabelBox) {
    flex-grow: 1;
  }
  :deep(.LabelText) {
    min-width: 4rem;
  }
  :deep(.TextField) {
    flex-grow: 1;
    overflow-x: auto;
  }
}
</style>
