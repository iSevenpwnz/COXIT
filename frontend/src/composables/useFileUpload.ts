/**
 * File upload composable with validation and drag & drop
 */
import { ref } from 'vue'

interface FileValidationError {
  type: 'size' | 'format'
  message: string
}

const MAX_FILE_SIZE_MB = 50
const ALLOWED_FILE_TYPE = 'application/pdf'

export function useFileUpload() {
  const isDragging = ref(false)
  const validationError = ref<FileValidationError | null>(null)

  const validateFile = (file: File): boolean => {
    validationError.value = null

    // Check file type
    if (file.type !== ALLOWED_FILE_TYPE) {
      validationError.value = {
        type: 'format',
        message: 'Please select a PDF file'
      }
      return false
    }

    // Check file size
    const sizeMB = file.size / (1024 * 1024)
    if (sizeMB > MAX_FILE_SIZE_MB) {
      validationError.value = {
        type: 'size',
        message: `File too large (maximum ${MAX_FILE_SIZE_MB}MB)`
      }
      return false
    }

    return true
  }

  const handleDragOver = (event: DragEvent) => {
    event.preventDefault()
    isDragging.value = true
  }

  const handleDragLeave = () => {
    isDragging.value = false
  }

  const handleDrop = (event: DragEvent): File | null => {
    event.preventDefault()
    isDragging.value = false

    const files = event.dataTransfer?.files
    if (!files || files.length === 0) {
      return null
    }

    const file = files[0]
    return validateFile(file) ? file : null
  }

  const handleFileSelect = (event: Event): File | null => {
    const target = event.target as HTMLInputElement
    const files = target.files
    
    if (!files || files.length === 0) {
      return null
    }

    const file = files[0]
    return validateFile(file) ? file : null
  }

  const clearError = () => {
    validationError.value = null
  }

  return {
    isDragging,
    validationError,
    validateFile,
    handleDragOver,
    handleDragLeave,
    handleDrop,
    handleFileSelect,
    clearError
  }
}