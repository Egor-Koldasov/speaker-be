<script setup lang="ts">
import { onMounted } from 'vue'
import { idb } from '../../idb/idb'
import { WsService } from '../../planning/WsService'
import { useLensUser } from '../../planning/DefineUseLens'

// # Props, State
// # Hooks
// # Computed
// # Callbacks
// # Watchers
onMounted(async () => {
  // void idb()
  WsService
  console.log('WsService', WsService)
})
const lensUser = useLensUser()
</script>
<template>
  <div>
    <div class="User">User</div>
    <pre>{{ JSON.stringify(lensUser.$state, undefined, 2) }}</pre>
  </div>
</template>
<style scoped lang="scss">
.User {
}
</style>
