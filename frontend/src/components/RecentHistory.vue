<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi, type HistoryItem } from '@/composables/useApi'
import { formatDate, formatNumber } from '@/utils/formatters'

const { fetchHistory, fetchSummary } = useApi()

const history = ref<HistoryItem[]>([])
const isLoading = ref(false)
const selectedSummary = ref<string>('')
const showSummaryModal = ref(false)
const error = ref<string | null>(null)

const loadHistory = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const result = await fetchHistory()
    
    if (result.error) {
      error.value = result.error
    } else if (result.data) {
      history.value = result.data
    }
  } catch (err) {
    error.value = 'Failed to load history'
  } finally {
    isLoading.value = false
  }
}

const viewSummary = async (summaryId: string) => {
  try {
    const result = await fetchSummary(summaryId)
    
    if (result.error) {
      error.value = result.error
    } else if (result.data) {
      selectedSummary.value = result.data
      showSummaryModal.value = true
    }
  } catch (err) {
    error.value = 'Failed to load summary'
  }
}

const closeSummaryModal = () => {
  showSummaryModal.value = false
  selectedSummary.value = ''
}

const clearError = () => {
  error.value = null
}

onMounted(() => {
  loadHistory()
})
</script>

<template>
  <div class="history-card">
    <div class="history-header">
      <h2>📚 Остання історія</h2>
      <button @click="loadHistory" class="refresh-btn" :disabled="isLoading">
        🔄 Оновити
      </button>
    </div>

    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>Завантаження...</p>
    </div>

    <div v-else-if="history.length === 0" class="empty-state">
      <div class="empty-icon">📭</div>
      <p>Історія порожня</p>
      <p class="empty-subtitle">Завантажте перший PDF щоб побачити його тут</p>
    </div>

    <div v-else class="history-list">
      <div 
        v-for="item in history" 
        :key="item.id" 
        class="history-item"
      >
        <div class="item-header">
          <div class="item-info">
            <h3 class="item-title">📄 PDF {{ item.id.slice(0, 8) }}...</h3>
            <p class="item-date">{{ formatDate(item.created_at) }}</p>
          </div>
          <button 
            @click="viewSummary(item.id)"
            class="view-btn"
          >
            👁️ Переглянути
          </button>
        </div>

        <div class="item-stats">
          <div class="stat-item">
            <span class="stat-icon">📄</span>
            <span>{{ item.pages }} стор.</span>
          </div>
          <div class="stat-item">
            <span class="stat-icon">💾</span>
            <span>{{ item.size_mb }}MB</span>
          </div>
          <div class="stat-item">
            <span class="stat-icon">📝</span>
            <span>{{ formatNumber(item.text_length) }} сим.</span>
          </div>
          <div class="stat-item">
            <span class="stat-icon">🖼️</span>
            <span>{{ item.images }} зобр.</span>
          </div>
          <div class="stat-item">
            <span class="stat-icon">📊</span>
            <span>{{ item.tables }} табл.</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal для відображення резюме -->
    <div v-if="showSummaryModal" class="modal-overlay" @click="closeSummaryModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>📝 AI Резюме</h3>
          <button @click="closeSummaryModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="summary-text">{{ selectedSummary }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.history-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.history-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.refresh-btn {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s ease;
}

.refresh-btn:hover:not(:disabled) {
  background: #059669;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #6b7280;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-subtitle {
  font-size: 0.9rem;
  color: #9ca3af;
  margin: 0.5rem 0 0 0;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.history-item {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.history-item:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.item-info h3 {
  margin: 0 0 0.25rem 0;
  color: #374151;
  font-size: 1.1rem;
}

.item-date {
  margin: 0;
  color: #6b7280;
  font-size: 0.85rem;
}

.view-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background 0.3s ease;
}

.view-btn:hover {
  background: #5a67d8;
}

.item-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: #f3f4f6;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  color: #374151;
}

.stat-icon {
  font-size: 0.9rem;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  color: #374151;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.close-btn:hover {
  background: #f3f4f6;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.summary-text {
  line-height: 1.6;
  color: #374151;
  white-space: pre-wrap;
}

@media (max-width: 768px) {
  .item-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .view-btn {
    align-self: flex-start;
  }
  
  .item-stats {
    gap: 0.5rem;
  }
  
  .stat-item {
    font-size: 0.75rem;
    padding: 0.3rem 0.6rem;
  }
}
</style>