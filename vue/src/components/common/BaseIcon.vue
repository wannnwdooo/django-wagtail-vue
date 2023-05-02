<template>
  <img :src="baseUrl + icon" alt="icon" />
</template>

<script lang="ts" setup>
const props = defineProps<{ icon: string }>()
const baseUrl = import.meta.env.VITE_BASE_URL
</script>

<style scoped></style>
