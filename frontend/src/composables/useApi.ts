/**
 * API composable for handling HTTP requests
 */
import { ref } from 'vue'

interface ApiResponse<T> {
  data: T | null
  error: string | null
  loading: boolean
}

interface UploadResult {
  id: string
  pages: number
  size_mb: number
  text_length: number
  images: number
  tables: number
  summary: string
}

interface HistoryItem {
  id: string
  filename: string
  summary_file: string
  created_at: string
  pages: number
  size_mb: number
  text_length: number
  images: number
  tables: number
}

interface HistoryResponse {
  history: HistoryItem[]
}

interface SummaryResponse {
  summary: string
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export function useApi() {
  const uploadFile = async (file: File): Promise<ApiResponse<UploadResult>> => {
    const loading = ref(true)
    const error = ref<string | null>(null)
    const data = ref<UploadResult | null>(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Upload failed')
      }

      data.value = await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
    } finally {
      loading.value = false
    }

    return {
      data: data.value,
      error: error.value,
      loading: loading.value
    }
  }

  const fetchHistory = async (): Promise<ApiResponse<HistoryItem[]>> => {
    const loading = ref(true)
    const error = ref<string | null>(null)
    const data = ref<HistoryItem[] | null>(null)

    try {
      const response = await fetch(`${API_BASE_URL}/history`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch history')
      }

      const result: HistoryResponse = await response.json()
      data.value = result.history
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load history'
    } finally {
      loading.value = false
    }

    return {
      data: data.value,
      error: error.value,
      loading: loading.value
    }
  }

  const fetchSummary = async (summaryId: string): Promise<ApiResponse<string>> => {
    const loading = ref(true)
    const error = ref<string | null>(null)
    const data = ref<string | null>(null)

    try {
      const response = await fetch(`${API_BASE_URL}/download/${summaryId}`)
      
      if (!response.ok) {
        throw new Error('Summary not found')
      }

      const result: SummaryResponse = await response.json()
      data.value = result.summary
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load summary'
    } finally {
      loading.value = false
    }

    return {
      data: data.value,
      error: error.value,
      loading: loading.value
    }
  }

  return {
    uploadFile,
    fetchHistory,
    fetchSummary
  }
}

export type { UploadResult, HistoryItem }