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
  original_filename: string
  file_hash: string
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

      const data = await response.json()
      
      return {
        data,
        error: null,
        loading: false
      }
    } catch (err) {
      return {
        data: null,
        error: err instanceof Error ? err.message : 'Unknown error occurred',
        loading: false
      }
    }
  }

  const fetchHistory = async (): Promise<ApiResponse<HistoryItem[]>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/history`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch history')
      }

      const result: HistoryResponse = await response.json()
      
      return {
        data: result.history,
        error: null,
        loading: false
      }
    } catch (err) {
      return {
        data: null,
        error: err instanceof Error ? err.message : 'Failed to load history',
        loading: false
      }
    }
  }

  const fetchSummary = async (summaryId: string): Promise<ApiResponse<string>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/download/${summaryId}`)
      
      if (!response.ok) {
        throw new Error('Summary not found')
      }

      const result: SummaryResponse = await response.json()
      
      return {
        data: result.summary,
        error: null,
        loading: false
      }
    } catch (err) {
      return {
        data: null,
        error: err instanceof Error ? err.message : 'Failed to load summary',
        loading: false
      }
    }
  }

  return {
    uploadFile,
    fetchHistory,
    fetchSummary
  }
}

export type { UploadResult, HistoryItem }