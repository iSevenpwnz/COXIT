import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { useApi } from '@/composables/useApi'

const mockFetch = vi.mocked(fetch)

describe('useApi', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('uploadFile', () => {
    it('should upload file successfully', async () => {
      const mockResponse = {
        id: 'test-id',
        pages: 10,
        size_mb: 1.5,
        text_length: 1000,
        images: 2,
        tables: 1,
        summary: 'Test summary'
      }

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      } as Response)

      const { uploadFile } = useApi()
      const file = new File(['test'], 'test.pdf', { type: 'application/pdf' })
      
      const result = await uploadFile(file)

      expect(result.data).toEqual(mockResponse)
      expect(result.error).toBeNull()
      expect(result.loading).toBe(false)
      
      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/upload',
        expect.objectContaining({
          method: 'POST',
          body: expect.any(FormData)
        })
      )
    })

    it('should handle upload error', async () => {
      const errorResponse = { detail: 'File too large' }

      mockFetch.mockResolvedValueOnce({
        ok: false,
        json: () => Promise.resolve(errorResponse)
      } as Response)

      const { uploadFile } = useApi()
      const file = new File(['test'], 'test.pdf', { type: 'application/pdf' })
      
      const result = await uploadFile(file)

      expect(result.data).toBeNull()
      expect(result.error).toBe('File too large')
      expect(result.loading).toBe(false)
    })

    it('should handle network error', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network error'))

      const { uploadFile } = useApi()
      const file = new File(['test'], 'test.pdf', { type: 'application/pdf' })
      
      const result = await uploadFile(file)

      expect(result.data).toBeNull()
      expect(result.error).toBe('Network error')
      expect(result.loading).toBe(false)
    })
  })

  describe('fetchHistory', () => {
    it('should fetch history successfully', async () => {
      const mockHistory = [
        {
          id: 'test-1',
          filename: 'test1.pdf',
          original_filename: 'Original Test 1.pdf',
          file_hash: 'hash1',
          summary_file: 'test1.txt',
          created_at: '2025-01-01T00:00:00',
          pages: 10,
          size_mb: 1.0,
          text_length: 1000,
          images: 2,
          tables: 1
        }
      ]

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ history: mockHistory })
      } as Response)

      const { fetchHistory } = useApi()
      const result = await fetchHistory()

      expect(result.data).toEqual(mockHistory)
      expect(result.error).toBeNull()
      expect(result.loading).toBe(false)
      
      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/history')
    })

    it('should handle fetch history error', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
      } as Response)

      const { fetchHistory } = useApi()
      const result = await fetchHistory()

      expect(result.data).toBeNull()
      expect(result.error).toBe('Failed to fetch history')
      expect(result.loading).toBe(false)
    })
  })

  describe('fetchSummary', () => {
    it('should fetch summary successfully', async () => {
      const mockSummary = 'This is a test summary'

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ summary: mockSummary })
      } as Response)

      const { fetchSummary } = useApi()
      const result = await fetchSummary('test-id')

      expect(result.data).toBe(mockSummary)
      expect(result.error).toBeNull()
      expect(result.loading).toBe(false)
      
      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/download/test-id')
    })

    it('should handle fetch summary error', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
      } as Response)

      const { fetchSummary } = useApi()
      const result = await fetchSummary('test-id')

      expect(result.data).toBeNull()
      expect(result.error).toBe('Summary not found')
      expect(result.loading).toBe(false)
    })
  })
})