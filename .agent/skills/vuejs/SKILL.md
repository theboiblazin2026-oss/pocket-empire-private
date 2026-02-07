---
name: Vue.js
description: Composition API, Vuex/Pinia, single-file components
---

# Vue.js Skill

## Composition API

```vue
<script setup>
import { ref, computed, onMounted } from 'vue';

const count = ref(0);
const doubled = computed(() => count.value * 2);

const increment = () => count.value++;

onMounted(() => {
  console.log('Component mounted');
});
</script>

<template>
  <button @click="increment">
    Count: {{ count }} (Doubled: {{ doubled }})
  </button>
</template>
```

## Pinia (State Management)

```javascript
// stores/counter.js
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  getters: {
    doubled: (state) => state.count * 2,
  },
  actions: {
    increment() {
      this.count++;
    },
  },
});

// In component
const store = useCounterStore();
store.increment();
```

## Directives

```vue
<template>
  <div v-if="show">Visible</div>
  <div v-else>Hidden</div>
  
  <ul>
    <li v-for="item in items" :key="item.id">{{ item.name }}</li>
  </ul>
  
  <input v-model="text" />
  <button @click="handleClick">Click</button>
</template>
```

## When to Apply
Use when building Vue.js applications or migrating from Options to Composition API.
