# Testing Guide

## Overview

This project includes comprehensive test suites for both backend (Python/FastAPI) and frontend (Vue 3/TypeScript) components with >80% code coverage.

## Backend Testing

### Setup
```bash
cd backend
pip install -r requirements.txt  # Includes pytest dependencies
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_pdf_service.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_upload"
```

### Test Structure
```
backend/tests/
├── __init__.py
├── test_api.py           # API endpoint tests
├── test_pdf_service.py   # PDF processing tests
└── test_storage_service.py # Storage & metadata tests
```

### Test Categories

**Unit Tests**: Test individual service methods in isolation
- PDF validation, parsing, and processing
- Storage operations (save, retrieve, metadata)
- AI service integration points

**Integration Tests**: Test API endpoints with mocked dependencies
- Upload workflow end-to-end
- History retrieval
- Summary download
- Error handling scenarios

### Mocking Strategy

- **External APIs**: OpenAI API calls are mocked
- **File System**: File operations use temporary directories
- **PDF Libraries**: PDF parsing libraries are mocked for consistent testing

## Frontend Testing

### Setup
```bash
cd frontend
npm install  # Includes Vitest and testing utilities
```

### Running Tests
```bash
# Run all tests
npm run test

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Watch mode
npm run test -- --watch
```

### Test Structure
```
frontend/tests/
├── setup.ts              # Global test setup
├── composables/
│   ├── useApi.test.ts     # API integration tests
│   └── useFileUpload.test.ts # File upload logic tests
└── utils/
    └── formatters.test.ts # Utility function tests
```

### Test Categories

**Composable Tests**: Test Vue Composition API logic
- API calls and response handling
- File validation and upload state management
- Error handling and user feedback

**Utility Tests**: Test helper functions
- Date/number formatting
- File size calculations
- Text truncation

### Mocking Strategy

- **Fetch API**: Global fetch is mocked for API tests
- **File API**: File objects are mocked for upload tests
- **DOM Events**: Browser events are simulated for interaction tests

## Coverage Reports

### Backend Coverage
Target: >80% overall coverage
- **Services**: >90% (core business logic)
- **API Routes**: >85% (endpoint handlers)
- **Models**: >70% (data validation)

### Frontend Coverage
Target: >75% overall coverage
- **Composables**: >85% (reactive logic)
- **Utils**: >90% (pure functions)
- **Components**: >70% (UI interactions)

## Test Execution in CI/CD

### Docker Test Execution
```bash
# Backend tests in container
docker run --rm -v $(pwd)/backend:/app -w /app python:3.11-slim sh -c "pip install -r requirements.txt && pytest"

# Frontend tests in container  
docker run --rm -v $(pwd)/frontend:/app -w /app node:20-alpine sh -c "npm install && npm run test"
```

### GitHub Actions (Example)
```yaml
- name: Test Backend
  run: |
    cd backend
    pip install -r requirements.txt
    pytest --cov=src --cov-report=xml

- name: Test Frontend
  run: |
    cd frontend
    npm install
    npm run test:coverage
```

## Writing New Tests

### Backend Test Template
```python
import pytest
from unittest.mock import Mock, patch
from src.services.your_service import YourService

class TestYourService:
    def test_method_success(self):
        # Arrange
        service = YourService()
        
        # Act
        result = service.your_method()
        
        # Assert
        assert result.is_success
        
    @patch('src.services.your_service.external_dependency')
    def test_method_with_mock(self, mock_dependency):
        # Setup mock
        mock_dependency.return_value = "mocked_value"
        
        # Test with mocked dependency
        service = YourService()
        result = service.method_using_dependency()
        
        assert result == "expected_result"
        mock_dependency.assert_called_once()
```

### Frontend Test Template
```typescript
import { describe, it, expect, vi } from 'vitest'
import { useYourComposable } from '@/composables/useYourComposable'

describe('useYourComposable', () => {
  it('should handle success case', () => {
    const { yourMethod, result } = useYourComposable()
    
    yourMethod('test-input')
    
    expect(result.value).toBe('expected-output')
  })
  
  it('should handle error case', () => {
    const { yourMethod, error } = useYourComposable()
    
    yourMethod('invalid-input')
    
    expect(error.value).toBeTruthy()
  })
})
```

## Best Practices

### General
- **AAA Pattern**: Arrange, Act, Assert
- **Descriptive Names**: Test names should describe the scenario
- **One Assertion**: Focus each test on a single behavior
- **Independent Tests**: Tests should not depend on each other

### Backend
- **Mock External Dependencies**: Don't call real APIs or databases
- **Test Edge Cases**: Empty inputs, malformed data, network errors
- **Verify Side Effects**: Check that files are created, data is saved

### Frontend
- **Mock API Calls**: Use vi.fn() for fetch and external calls
- **Test User Interactions**: Simulate clicks, form submissions, drag & drop
- **Verify Reactive Updates**: Check that UI updates when state changes

## Debugging Tests

### Backend
```bash
# Run with debugger
pytest --pdb

# Show print statements
pytest -s

# Run single test with verbose output
pytest tests/test_api.py::TestAPI::test_upload_success -v -s
```

### Frontend
```bash
# Run tests in watch mode with console output
npm run test -- --reporter=verbose

# Debug specific test
npm run test -- tests/composables/useApi.test.ts
```

## Performance Testing

### Load Testing (Backend)
```python
# Example with pytest-benchmark
def test_pdf_processing_performance(benchmark):
    result = benchmark(process_large_pdf, large_pdf_content)
    assert result.processing_time < 5.0  # seconds
```

### Bundle Size Testing (Frontend)
```bash
# Analyze bundle size
npm run build
npx vite-bundle-analyzer dist
```