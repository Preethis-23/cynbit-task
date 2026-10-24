"""
Schemas for document ingestion and text preprocessing.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """Metadata about ingested client requirement document."""

    source_type: Literal["text", "pdf", "docx", "sample"] = Field(
        ..., description="Origin source format"
    )
    filename: Optional[str] = Field(default=None, description="Original filename if uploaded")
    char_count: int = Field(default=0, ge=0)
    word_count: int = Field(default=0, ge=0)
    paragraph_count: int = Field(default=0, ge=0)
    warnings: list[str] = Field(default_factory=list)


class IngestedDocument(BaseModel):
    """Container holding cleaned text and metadata."""

    raw_text: str
    cleaned_text: str
    metadata: DocumentMetadata
