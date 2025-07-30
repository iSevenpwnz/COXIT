<script setup lang="ts">
import { onMounted } from 'vue'
import PdfUploader from './components/PdfUploader.vue'
import RecentHistory from './components/RecentHistory.vue'

onMounted(() => {
  console.log('PDF Summary AI App завантажено')
})
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>📄 PDF Summary AI</h1>
      <p>Завантажте PDF та отримайте AI-резюме за лічені секунди</p>
    </header>
    
    <main class="main">
      <div class="container">
        <PdfUploader />
        <RecentHistory />
      </div>
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header {
  text-align: center;
  padding: 2rem 1rem;
  color: white;
}

.header h1 {
  font-size: 3rem;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.header p {
  font-size: 1.2rem;
  margin: 1rem 0 0 0;
  opacity: 0.9;
}

.main {
  padding: 0 1rem 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 768px) {
  .container {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
