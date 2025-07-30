import { describe, it, expect, vi } from 'vitest'
import { useFileUpload } from '@/composables/useFileUpload'

// Mock DragEvent for jsdom environment
class MockDragEvent extends Event {
  dataTransfer: DataTransfer | null = null

  constructor(type: string, eventInitDict?: EventInit) {
    super(type, eventInitDict)
  }
}

// Add it to global scope
global.DragEvent = MockDragEvent as any

describe('useFileUpload', () => {
  describe('validateFile', () => {
    it('should validate PDF file successfully', () => {
      const { validateFile } = useFileUpload()
      const file = new File(['test'], 'test.pdf', { type: 'application/pdf' })
      
      const result = validateFile(file)
      expect(result).toBe(true)
    })

    it('should reject non-PDF file', () => {
      const { validateFile, validationError } = useFileUpload()
      const file = new File(['test'], 'test.txt', { type: 'text/plain' })
      
      const result = validateFile(file)
      expect(result).toBe(false)
      expect(validationError.value?.type).toBe('format')
      expect(validationError.value?.message).toBe('Please select a PDF file')
    })

    it('should reject oversized file', () => {
      const { validateFile, validationError } = useFileUpload()
      // Create mock file that appears to be > 50MB
      const file = new File(['x'.repeat(51 * 1024 * 1024)], 'large.pdf', { 
        type: 'application/pdf' 
      })
      
      const result = validateFile(file)
      expect(result).toBe(false)
      expect(validationError.value?.type).toBe('size')
      expect(validationError.value?.message).toContain('File too large')
    })
  })

  describe('drag and drop handlers', () => {
    it('should handle drag over', () => {
      const { handleDragOver, isDragging } = useFileUpload()
      const event = new DragEvent('dragover')
      const preventDefaultSpy = vi.spyOn(event, 'preventDefault')
      
      handleDragOver(event)
      
      expect(preventDefaultSpy).toHaveBeenCalled()
      expect(isDragging.value).toBe(true)
    })

    it('should handle drag leave', () => {
      const { handleDragLeave, isDragging } = useFileUpload()
      
      // First set dragging to true
      isDragging.value = true
      
      handleDragLeave()
      
      expect(isDragging.value).toBe(false)
    })

    it('should handle drop with valid file', () => {
      const { handleDrop, isDragging } = useFileUpload()
      
      const file = new File(['test'], 'test.pdf', { type: 'application/pdf' })
      const dataTransfer = {
        files: [file] as any
      }
      
      const event = new DragEvent('drop')
      Object.defineProperty(event, 'dataTransfer', {
        value: dataTransfer
      })
      const preventDefaultSpy = vi.spyOn(event, 'preventDefault')
      
      // Set dragging to true first
      isDragging.value = true
      
      const result = handleDrop(event)
      
      expect(preventDefaultSpy).toHaveBeenCalled()
      expect(isDragging.value).toBe(false)
      expect(result).toBe(file)
    })

    it('should handle drop with no files', () => {
      const { handleDrop } = useFileUpload()
      
      const event = new DragEvent('drop')
      Object.defineProperty(event, 'dataTransfer', {
        value: { files: [] }
      })
      
      const result = handleDrop(event)
      
      expect(result).toBeNull()
    })
  })

  describe('file select handler', () => {
    it('should handle file select with valid file', () => {
      const { handleFileSelect } = useFileUpload()
      
      const file = new File(['test'], 'test.pdf', { type: 'application/pdf' })
      const input = document.createElement('input')
      input.type = 'file'
      
      // Mock the files property
      Object.defineProperty(input, 'files', {
        value: [file],
        writable: false,
      })
      
      const event = new Event('change')
      Object.defineProperty(event, 'target', {
        value: input
      })
      
      const result = handleFileSelect(event)
      
      expect(result).toBe(file)
    })

    it('should handle file select with no files', () => {
      const { handleFileSelect } = useFileUpload()
      
      const input = document.createElement('input')
      input.type = 'file'
      
      Object.defineProperty(input, 'files', {
        value: [],
        writable: false,
      })
      
      const event = new Event('change')
      Object.defineProperty(event, 'target', {
        value: input
      })
      
      const result = handleFileSelect(event)
      
      expect(result).toBeNull()
    })
  })

  describe('clearError', () => {
    it('should clear validation error', () => {
      const { validateFile, clearError, validationError } = useFileUpload()
      
      // First create an error
      const file = new File(['test'], 'test.txt', { type: 'text/plain' })
      validateFile(file)
      
      expect(validationError.value).not.toBeNull()
      
      clearError()
      
      expect(validationError.value).toBeNull()
    })
  })
})