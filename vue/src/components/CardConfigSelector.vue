<script setup lang="ts">
import { useLensQueryUserCardConfigs } from '../planning/Lens/useLensQueryUserCardConfigs'
import LabelBox from './ui/LabelBox.vue'
import LabelText from './ui/LabelText.vue'
import Select from './ui/Select.vue'
import Option from './ui/Option.vue'
import { useCardConfigSelector } from '../uiStore/useCardConfigSelector'

// # Props, State
// # Hooks
const userCardConfig = useLensQueryUserCardConfigs()
const cardConfigSelector = useCardConfigSelector()
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <LabelBox class="CardConfigSelector">
    <LabelText class="label-text">Card config</LabelText>
    <Select
      :value="cardConfigSelector.selectedCardConfigId"
      @change="
        (nextId) => {
          cardConfigSelector.$state.selectedCardConfigId = nextId
        }
      "
    >
      <Option value=""></Option>
      <Option
        v-for="cardConfig in userCardConfig.$state.memData.cardConfigs"
        :key="cardConfig.id"
        :value="cardConfig.id"
      >
        {{ cardConfig.name }}
      </Option>
    </Select>
  </LabelBox>
</template>
<style scoped lang="scss">
.CardConfigSelector {
  .Select::v-deep {
    flex-grow: 1;
  }
}
</style>
