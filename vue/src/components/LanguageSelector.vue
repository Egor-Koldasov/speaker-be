<script setup lang="ts">
import tags from 'language-tags'
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { uniqBy } from 'lodash'
import { nonNull } from '../util/nonNull'
import { isNodeOrParent } from '../util/isNodeOrParent'

// # Props, State
const props = defineProps<{
  languageBcp47List: string[]
  onAddLanguageBcp47: (languageBcp47: string) => void
  onRemoveLanguageBcp47: (languageBcp47: string) => void
}>()
const ui = reactive({
  open: false,
  searchString: '',
})
const inputRef = ref<HTMLInputElement | null>(null)
const componentRef = ref<HTMLDivElement | null>(null)
// # Hooks
// # Computed
const languageOptions = computed(() => searchLanguage(ui.searchString))
// # Callbacks
const searchLanguage = (searchString: string) => {
  const languageList = searchString ? tags.search(searchString) : []
  const selectedLanguageList = props.languageBcp47List
    .map((language) => tags.language(language))
    .filter(nonNull)

  const combinedList = [...selectedLanguageList, ...languageList]
  const uniqList = uniqBy(combinedList, (language) =>
    language.format().toLowerCase(),
  ).sort((a, b) => (props.languageBcp47List.includes(a.format()) ? -1 : 1))
  return uniqList
}
const onInputFocus = () => {
  ui.open = true
}
const onClickOutside = (event: Event) => {
  if (
    event.target &&
    componentRef.value &&
    isNodeOrParent(event.target as Node, componentRef.value)
  ) {
    return
  }
  ui.open = false
}
// # Watchers
onMounted(() => {
  window.addEventListener('click', onClickOutside)
})
onUnmounted(() => {
  window.removeEventListener('click', onClickOutside)
})
</script>
<template>
  <div
    class="dropdown LanguageSelector"
    :class="{ open: ui.open }"
    ref="componentRef"
  >
    <summary class="header" @click.prevent="inputRef?.focus()">
      <span class="language-code-list">
        <span
          class="language-code"
          v-for="language in props.languageBcp47List"
          :key="language"
          >{{ language }}</span
        >
      </span>

      <input
        type="text"
        v-model="ui.searchString"
        @focus="onInputFocus"
        @blur="onClickOutside"
        ref="inputRef"
        @keydown.escape="ui.open = false"
      />
    </summary>
    <ul class="dropdown-panel" :class="{ empty: languageOptions.length === 0 }">
      <li
        v-for="language in languageOptions"
        :key="language.format()"
        @click="
          () =>
            props.languageBcp47List.includes(language.format())
              ? props.onRemoveLanguageBcp47(language.format())
              : props.onAddLanguageBcp47(language.format())
        "
      >
        <input
          type="checkbox"
          :checked="props.languageBcp47List.includes(language.format())"
        />
        <span class="language-code">
          {{ language.format() }}
        </span>
        <span class="language-description">{{
          ' ' + language.descriptions().join(', ')
        }}</span>
      </li>
    </ul>
  </div>
</template>
<style scoped lang="scss">
.LanguageSelector.LanguageSelector {
  position: relative;
  background-color: #ffffff16;
  border-radius: 0.2rem;
  min-width: 40px;
  .header {
    padding: 0;
    display: flex;
    align-items: center;
    border: none;
    gap: 0;
    height: 30px;

    .language-code-list {
      padding: 0 0.5rem;
      display: flex;
      gap: 0.2rem;
    }

    input {
      width: 0;
      padding: 0;
      border: none;
      height: 100%;
      background-color: transparent;
      &:focus {
        outline: none;
        box-shadow: none;
      }
    }

    &::after {
      margin: 0 0.2rem;
    }
    &:focus {
      outline: none;
      box-shadow: none;
    }
  }
  .language-code {
    font-weight: 700;
    color: var(--pico-primary);
    text-transform: uppercase;
  }

  .language-description {
  }

  .dropdown-panel {
    left: auto;
    right: 0;
    width: 100%;
    min-width: auto;
    overflow: hidden;
    max-height: 0;
    position: absolute;
    top: 100%;
    padding: 0;
    background-color: inherit;
    border-radius: 0 0 0.2rem 0.2rem;

    li {
      text-wrap: wrap;
      cursor: pointer;
      list-style: none;
      margin: 0;
      padding: 0 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.3rem;

      input[type='checkbox'] {
        width: 1rem;
        height: 1rem;
      }

      &:hover {
        background-color: #50214b;
        color: white;
      }
    }
  }
  &.open {
    .header {
      input {
        width: 150px;
      }
    }
    .dropdown-panel:not(.empty) {
      max-height: 90vh;
      border-top: 1px solid #ffffff22;
    }
  }
}
</style>
