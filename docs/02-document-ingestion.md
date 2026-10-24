# Phase 2: Document Ingestion

Implement the input layer for the Cynbit AI Pre-Sales Solution Architect.

## Objective

Allow a user to provide a project brief as plain text or an uploaded PDF/DOCX file and convert it into clean text for analysis.

## Tasks

1. Add Streamlit upload and text-input controls.
2. Extract text from supported files.
3. Normalize whitespace and remove obvious extraction noise.
4. Show a preview before analysis.
5. Validate file type, size, and empty content.
6. Return useful errors without exposing sensitive content in logs.

## Output contract

Return a document object containing:

- source type
- original filename when available
- extracted text
- character/word count
- warnings

## Constraints

- Keep ingestion separate from LLM logic.
- Do not send data to an external provider until the user starts analysis.
- Avoid storing uploaded files permanently.

## Completion criteria

- Plain text works.
- PDF and DOCX extraction works or fails with a clear message.
- Empty, oversized, and unsupported files are handled.
- The extracted text can be passed to Phase 3.
