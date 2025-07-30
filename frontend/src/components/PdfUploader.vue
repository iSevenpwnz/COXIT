<script setup lang="ts">
import { ref } from 'vue'
import { useApi, type UploadResult } from '@/composables/useApi'
import { useFileUpload } from '@/composables/useFileUpload'
import { formatNumber } from '@/utils/formatters'

const { uploadFile } = useApi()
const {
  isDragging,
  validationError,
  handleDragOver,
  handleDragLeave,
  handleDrop,
  handleFileSelect,
  clearError
} = useFileUpload()

const isUploading = ref(false)
const uploadResult = ref<UploadResult | null>(null)
const uploadError = ref<string | null>(null)

const processFileUpload = async (file: File | null) => {
  if (!file) return

  clearError()
  uploadError.value = null
  isUploading.value = true
  uploadResult.value = null

  try {
    const result = await uploadFile(file)
    
    if (result.error) {
      uploadError.value = result.error
    } else if (result.data) {
      uploadResult.value = result.data
    }
  } catch (error) {
    uploadError.value = error instanceof Error ? error.message : 'Upload failed'
  } finally {
    isUploading.value = false
  }
}

const onFileSelect = (event: Event) => {
  const file = handleFileSelect(event)
  processFileUpload(file)
}

const onFileDrop = (event: DragEvent) => {
  const file = handleDrop(event)
  processFileUpload(file)
}

const resetUpload = () => {
  uploadResult.value = null
  uploadError.value = null
  clearError()
}
</script>

<template>
  <div class="uploader-card">
    <h2>📤 Завантажити PDF</h2>
    
    <div v-if="!uploadResult" class="upload-area">
      <div 
        class="drop-zone"
        :class="{ 'dragging': isDragging, 'uploading': isUploading }"
        @drop="onFileDrop"
        @dragover="handleDragOver"
        @dragleave="handleDragLeave"
      >
        <div v-if="isUploading" class="loading">
          <div class="spinner"></div>
          <p>Обробка PDF...</p>
        </div>
        
        <div v-else class="drop-content">
          <div class="upload-icon">📄</div>
          <p class="upload-text">Перетягніть PDF сюди або</p>
          <label for="file-input" class="upload-btn">
            Оберіть файл
          </label>
          <input
            id="file-input"
            type="file"
            accept=".pdf"
            @change="onFileSelect"
            style="display: none"
          >
          <p class="file-info">Максимум 100 сторінок, 50MB</p>
        </div>
      </div>
      
      <div v-if="validationError || uploadError" class="error">
        ❌ {{ validationError?.message || uploadError }}
      </div>
    </div>

    <div v-if="uploadResult" class="result">
      <div class="result-header">
        <h3>✅ PDF успішно оброблено!</h3>
        <button @click="resetUpload" class="reset-btn">Завантажити інший</button>
      </div>
      
      <div class="result-stats">
        <div class="stat">
          <span class="stat-label">Сторінок:</span>
          <span class="stat-value">{{ uploadResult.pages }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Розмір:</span>
          <span class="stat-value">{{ uploadResult.size_mb }}MB</span>
        </div>
        <div class="stat">
          <span class="stat-label">Текст:</span>
          <span class="stat-value">{{ formatNumber(uploadResult.text_length) }} символів</span>
        </div>
        <div class="stat">
          <span class="stat-label">Зображення:</span>
          <span class="stat-value">{{ uploadResult.images }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Таблиці:</span>
          <span class="stat-value">{{ uploadResult.tables }}</span>
        </div>
      </div>

      <div class="summary">
        <h4>📝 AI Резюме:</h4>
        <div class="summary-text">{{ uploadResult.summary }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.uploader-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.uploader-card h2 {
  margin: 0 0 1.5rem 0;
  color: #333;
  font-size: 1.5rem;
}

.drop-zone {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 3rem;
  text-align: center;
  transition: all 0.3s ease;
  background: #fafafa;
}

.drop-zone.dragging {
  border-color: #667eea;
  background: #f0f4ff;
}

.drop-zone.uploading {
  border-color: #667eea;
  background: #f0f4ff;
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.upload-text {
  font-size: 1.1rem;
  color: #666;
  margin: 0 0 1rem 0;
}

.upload-btn {
  display: inline-block;
  background: #667eea;
  color: white;
  padding: 0.8rem 2rem;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s ease;
}

.upload-btn:hover {
  background: #5a67d8;
}

.file-info {
  font-size: 0.9rem;
  color: #999;
  margin: 1rem 0 0 0;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  background: #fee;
  color: #c53030;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  text-align: center;
}

.result {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.result-header h3 {
  margin: 0;
  color: #22c55e;
}

.reset-btn {
  background: #6b7280;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.reset-btn:hover {
  background: #4b5563;
}

.result-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat {
  background: #f8fafc;
  padding: 0.8rem;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
}

.stat-label {
  color: #64748b;
  font-weight: 500;
}

.stat-value {
  color: #1e293b;
  font-weight: bold;
}

.summary {
  background: #f0f9ff;
  border: 1px solid #e0f2fe;
  border-radius: 8px;
  padding: 1.5rem;
}

.summary h4 {
  margin: 0 0 1rem 0;
  color: #0369a1;
}

.summary-text {
  line-height: 1.6;
  color: #374151;
  white-space: pre-wrap;
}
</style>