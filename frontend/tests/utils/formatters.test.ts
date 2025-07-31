import { describe, it, expect } from 'vitest'
import { formatDate, formatFileSize, formatNumber, truncateText } from '@/utils/formatters'

describe('formatters', () => {
  describe('formatDate', () => {
    it('should format ISO date string to localized format', () => {
      const isoString = '2025-01-15T14:30:00.000Z'
      const result = formatDate(isoString)
      
      // Result will depend on locale, but should be a string
      expect(typeof result).toBe('string')
      expect(result.length).toBeGreaterThan(0)
    })
  })

  describe('formatFileSize', () => {
    it('should format size less than 1MB to KB', () => {
      const result = formatFileSize(0.5)
      expect(result).toBe('512KB')
    })

    it('should format size greater than 1MB to MB', () => {
      const result = formatFileSize(1.5)
      expect(result).toBe('1.5MB')
    })

    it('should handle zero size', () => {
      const result = formatFileSize(0)
      expect(result).toBe('0KB')
    })
  })

  describe('formatNumber', () => {
    it('should format number with thousand separators', () => {
      const result = formatNumber(1234567)
      // Should have separators (format depends on locale)
      expect(typeof result).toBe('string')
      expect(result.length).toBeGreaterThan(7) // Should have separators
    })

    it('should handle small numbers', () => {
      const result = formatNumber(123)
      expect(result).toBe('123')
    })

    it('should handle zero', () => {
      const result = formatNumber(0)
      expect(result).toBe('0')
    })
  })

  describe('truncateText', () => {
    it('should truncate text longer than maxLength', () => {
      const text = 'This is a very long text that should be truncated'
      const result = truncateText(text, 20)
      
      expect(result).toBe('This is a very long ...')
      expect(result.length).toBe(23) // 20 + 3 dots
    })

    it('should return original text if shorter than maxLength', () => {
      const text = 'Short text'
      const result = truncateText(text, 20)
      
      expect(result).toBe(text)
    })

    it('should handle exact length match', () => {
      const text = 'Exactly twenty chars'
      const result = truncateText(text, 20)
      
      expect(result).toBe(text)
    })

    it('should handle empty string', () => {
      const result = truncateText('', 10)
      expect(result).toBe('')
    })
  })
})