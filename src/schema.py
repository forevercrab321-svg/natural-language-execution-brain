"""
Data structures for intent parsing and execution briefs.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from enum import Enum


class ExecutionMode(Enum):
    """Supported execution modes."""
    DIRECT_EXECUTE = "direct_execute"
    AUTONOMOUS_EXECUTE = "autonomous_execute"
    ANALYZE_THEN_EXECUTE = "analyze_then_execute"
    DRAFT_THEN_EXECUTE = "draft_then_execute"
    APPROVAL_GATED_EXECUTE = "approval_gated_execute"
    MONITOR_ONLY = "monitor_only"


class UrgencyLevel(Enum):
    """Urgency levels for task execution."""
    HIGH = "high"
    NORMAL = "normal"
    DEFERRED = "deferred"


@dataclass
class IntentParse:
    """
    Structured representation of parsed user intent.
    """
    
    intent_summary: str
    real_goal: str
    deliverable: str
    
    hard_constraints: List[str] = field(default_factory=list)
    soft_preferences: List[str] = field(default_factory=list)
    forbidden_actions: List[str] = field(default_factory=list)
    approval_boundaries: List[str] = field(default_factory=list)
    
    assumptions: List[str] = field(default_factory=list)
    
    execution_mode: str = "direct_execute"
    urgency: str = "normal"
    
    next_actions: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    fallback_plan: List[str] = field(default_factory=list)
    
    confidence: float = 0.85
    ambiguity_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


@dataclass
class ExecutionBrief:
    """Execution-ready brief derived from IntentParse."""
    
    task_id: str
    intent_parse: IntentParse
    
    primary_objective: str
    gated_items: List[Dict[str, str]] = field(default_factory=list)
    autonomous_items: List[str] = field(default_factory=list)
    
    should_ask_for_approval: bool = False
    should_operate_autonomously: bool = True
    should_report_status: bool = False
    reporting_threshold: str = "material_changes_only"
    
    status: str = "ready"
    blocked_reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ActionPlan:
    """Ordered sequence of actions to execute."""
    
    plan_id: str
    intent_parse: IntentParse
    
    actions: List[Dict[str, Any]] = field(default_factory=list)
    
    execution_order: str = "sequential"
    failure_mode: str = "stop_on_first_error"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ParseResult:
    """Complete result of intent parsing operation."""
    
    original_text: str
    parsed_intent: IntentParse
    execution_brief: ExecutionBrief
    action_plan: ActionPlan
    
    parsing_confidence: float
    interpretation_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "original_text": self.original_text,
            "parsed_intent": self.parsed_intent.to_dict(),
            "execution_brief": self.execution_brief.to_dict(),
            "action_plan": self.action_plan.to_dict(),
            "parsing_confidence": self.parsing_confidence,
            "interpretation_notes": self.interpretation_notes,
        }
