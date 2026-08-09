"""
===============================================================================
SCHEMAS: ACTION ITEMS & MEETING OUTPUTS METADATA
===============================================================================
Pydantic schemas for extracted action items, task assignment, and generated outputs.
===============================================================================
"""

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from schemas.common_schema import ActionItemStatusEnum


class ActionItemBase(BaseModel):
    """Base fields for meeting action items."""
    task: str = Field(..., min_length=1, description="Description of the action item task")
    owner: Optional[str] = Field(None, max_length=255, description="Person responsible for the task")
    due_date: Optional[date] = Field(None, description="Due date for completion")
    status: ActionItemStatusEnum = Field(ActionItemStatusEnum.OPEN, description="Task status")


class ActionItemCreate(ActionItemBase):
    """Schema for creating an action item in database."""
    meeting_id: str = Field(..., description="Parent meeting ID")


class ActionItemUpdate(BaseModel):
    """Schema for updating an existing action item."""
    task: Optional[str] = Field(None, min_length=1, description="Updated task text")
    owner: Optional[str] = Field(None, max_length=255, description="Updated task owner")
    due_date: Optional[date] = Field(None, description="Updated due date")
    status: Optional[ActionItemStatusEnum] = Field(None, description="Updated status")


class ActionItemResponse(ActionItemBase):
    """Complete action item record from database."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Unique UUID of the action item")
    meeting_id: str = Field(..., description="Parent meeting ID")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")


class MeetingOutputMetaResponse(BaseModel):
    """Metadata schema for generated meeting outputs (summary, key decisions, PDF, etc.)."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Unique output record UUID")
    meeting_id: str = Field(..., description="Parent meeting ID")
    output_type: str = Field(..., max_length=30, description="Output type (e.g. 'summary', 'action_items', 'pdf')")
    generated_at: Optional[datetime] = Field(None, description="Generation timestamp")
