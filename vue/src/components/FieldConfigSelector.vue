<script setup lang="ts">
import { useLensQueryUserCardConfigs } from '../planning/Lens/useLensQueryUserCardConfigs'
import LabelBox from './ui/LabelBox.vue'
import LabelText from './ui/LabelText.vue'
import Select from './ui/Select.vue'
import Option from './ui/Option.vue'
import { useCardConfigSelector } from '../uiStore/useCardConfigSelector'
import { useFieldConfigSelector } from '../uiStore/useFieldConfigSelector'

// # Props, State
// # Hooks
const userCardConfig = useLensQueryUserCardConfigs()
const fieldConfigSelector = useFieldConfigSelector()
// # Computed
// # Callbacks
// # Watchers
</script>
<template>
  <LabelBox class="FieldConfigSelector">
    <LabelText class="label-text">Field config</LabelText>
    <Select
      :value="fieldConfigSelector.selectedFieldConfigId"
      @change="
        (nextId) => {
          fieldConfigSelector.$state.selectedFieldConfigId = nextId
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
.FieldConfigSelector {
  flex-grow: 1;
  background-color: #39293f;
  box-shadow: 0 3px 0px 0px #231927;
  border-top-left-radius: 0.4rem;
  border-bottom-left-radius: 0.4rem;
  .label-text {
    padding: 0 0.4rem;
    flex-shrink: 0;
  }
  :deep(.Select) {
    flex-grow: 1;
    flex-shrink: 1;
    background-color: transparent;
  }
}
</style>
