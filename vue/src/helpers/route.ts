import { useRoute } from 'vue-router'
import { computed } from 'vue'

const urlSplit = (path: string, targetPath: string) => {
  const parts = path.split('/')
  const urlSplit = parts.length === 2 || (parts.length === 3 && parts[2] === '')
  return urlSplit && path.startsWith(targetPath)
};

// Объявление функции
export const checkNonNestedPage = (targetPath: string) => {
  const route = useRoute()
  return computed(() => {
    const path = route.path
    return urlSplit(path, targetPath)
  })
};
