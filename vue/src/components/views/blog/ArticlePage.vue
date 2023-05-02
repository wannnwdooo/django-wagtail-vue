<template>
  <div>
    <h2>{{ article }}</h2>
    <p>Контент статьи</p>
    <button @click="$router.push({ path: `/blog/` })">На страницу блога</button>
    <BaseImage v-if="result.blog_image" :image="result.blog_image" />
    <BaseIcon icon="/media/assets/1.svg"/>
  </div>
</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue'
import { getOneBlog } from '@/services/blog.service'
import BaseImage from '@/components/common/BaseImage.vue'
import BaseIcon from "@/components/common/BaseIcon.vue";

defineProps<{ article: string }>()
const route = useRoute()

const result = ref({ blog_image: '' })

onMounted(async () => {
  result.value = await getOneBlog(route.query.id)
})
</script>

<style scoped></style>
