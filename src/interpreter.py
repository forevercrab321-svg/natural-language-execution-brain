"""Main interpreter module: NaturalLanguageExecutionBrain."""

from __future__ import annotations
from dataclasses import asdict
from typing import Optional
import json
import uuid

from src.schema import IntentParse, ExecutionBrief, ActionPlan, ParseResult
from src.intent_parser import IntentParser
from src import utils


class NaturalLanguageExecutionBrain:
    """Main brain for parsing natural language into executable intent."""
    
    def __init__(self):
        self.parser = IntentParser()
    
    def parse_user_intent(self, user_text: str) -> IntentParse:
        """Parse user natural language into structured intent."""
        user_text = user_text.strip()
        
        intent_summary = self.parser.build_intent_summary(user_text)
        real_goal = self.parser.infer_real_goal(user_text)
        deliverable = self.parser.infer_deliverable(user_text)
        hard_constraints = self.parser.extract_hard_constraints(user_text)
        soft_preferences = self.parser.extract_soft_preferences(user_text)
        forbidden_actions = self.parser.extract_forbidden_actions(user_text)
        approval_boundaries = self.parser.detect_approval_boundaries(user_text)
        assumptions = self.parser.resolve_assumptions(user_text)
        execution_mode = self.parser.infer_execution_mode(user_text)
        urgency = self.parser.infer_urgency(user_text)
        next_actions = self.parser.translate_to_actions(user_text, real_goal, deliverable)
        success_criteria = self.parser.build_success_criteria(real_goal, deliverable)
        fallback_plan = self.parser.build_fallback_plan(user_text)
        
        emotional, _ = utils.detect_emotional_language(user_text)
        explicit_clarity = 1 if len(user_text) > 30 else 0.7
        ambiguity_count = utils.count_negations(user_text)
        confidence = utils.infer_confidence(
            explicit_requests=1 if explicit_clarity > 0.7 else 0,
            implied_goals=1 if real_goal != intent_summary else 0,
            ambiguity_count=ambiguity_count,
        )
        
        ambiguity_notes = ""
        if emotional:
            ambiguity_notes += "Emotional language detected; interpreting as operational directive. "
        if not approval_boundaries and utils.contains_any_keyword(user_text, self.parser.autonomy_keywords):
            ambiguity_notes += "No explicit approval gates specified; inferring autonomous execution on all items."
        
        return IntentParse(
            intent_summary=intent_summary,
            real_goal=real_goal,
            deliverable=deliverable,
            hard_constraints=hard_constraints,
            soft_preferences=soft_preferences,
            forbidden_actions=forbidden_actions,
            approval_boundaries=approval_boundaries,
            assumptions=assumptions,
            execution_mode=execution_mode,
            urgency=urgency,
            next_actions=next_actions,
            success_criteria=success_criteria,
            fallback_plan=fallback_plan,
            confidence=confidence,
            ambiguity_notes=ambiguity_notes,
        )
    
    def build_execution_brief(self, intent_parse: IntentParse) -> ExecutionBrief:
        """Build an execution-ready brief from parsed intent."""
        task_id = str(uuid.uuid4())[:8]
        
        gated_items = []
        autonomous_items = intent_parse.next_actions.copy()
        
        for boundary in intent_parse.approval_boundaries:
            gated_items.append({
                "item": f"Items requiring {boundary}",
                "gate": boundary,
            })
        
        should_ask = len(intent_parse.approval_boundaries) > 0
        
        should_operate_autonomously = (
            intent_parse.execution_mode == "autonomous_execute" or
            intent_parse.execution_mode == "direct_execute" or
            intent_parse.execution_mode == "approval_gated_execute"
        )
        
        reporting_threshold = "material_changes_only"
        
        return ExecutionBrief(
            task_id=task_id,
            intent_parse=intent_parse,
            primary_objective=intent_parse.real_goal,
            gated_items=gated_items,
            autonomous_items=autonomous_items,
            should_ask_for_approval=should_ask,
            should_operate_autonomously=should_operate_autonomously,
            should_report_status=False,
            reporting_threshold=reporting_threshold,
            status="ready",
        )
    
    def build_action_plan(
        self,
        intent_parse: IntentParse,
        execution_brief: Optional[ExecutionBrief] = None,
    ) -> ActionPlan:
        """Build an ordered action plan from intent."""
        if execution_brief is None:
            execution_brief = self.build_execution_brief(intent_parse)
        
        plan_id = str(uuid.uuid4())[:8]
        
        actions = []
        for i, action_desc in enumerate(intent_parse.next_actions, 1):
            action = {
                "id": f"action_{i}",
                "description": action_desc,
                "type": "execute",
                "parameters": {},
                "requires_approval": False,
                "depends_on": [f"action_{i-1}"] if i > 1 else [],
            }
            actions.append(action)
        
        execution_order = "sequential"
        
        return ActionPlan(
            plan_id=plan_id,
            intent_parse=intent_parse,
            actions=actions,
            execution_order=execution_order,
            failure_mode="stop_on_first_error",
        )
    
    def parse_and_brief(self, user_text: str) -> tuple:
        """Parse intent and create execution brief in one call."""
        intent_parse = self.parse_user_intent(user_text)
        execution_brief = self.build_execution_brief(intent_parse)
        return intent_parse, execution_brief
    
    def parse_full_result(self, user_text: str) -> ParseResult:
        """Complete parsing pipeline: intent -> brief -> action plan."""
        intent_parse = self.parse_user_intent(user_text)
        execution_brief = self.build_execution_brief(intent_parse)
        action_plan = self.build_action_plan(intent_parse, execution_brief)
        
        return ParseResult(
            original_text=user_text,
            parsed_intent=intent_parse,
            execution_brief=execution_brief,
            action_plan=action_plan,
            parsing_confidence=intent_parse.confidence,
            interpretation_notes=intent_parse.ambiguity_notes,
        )


if __name__ == "__main__":
    brain = NaturalLanguageExecutionBrain()
    
    test_cases = [
        "你给我写一个skill，提升agent得理解能力，就是在我们用自然语言描述的时候，他能准确理解我们的意思并转成行动。我放到VS Code里面写。",
        "别老汇报，直接推进。除非付款和法律文件，不要来问我。",
        "你别分析，直接给我能发给团队执行的东西。",
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}:")
        print(f"{'='*60}")
        print(f"User: {test_case}\n")
        
        result = brain.parse_full_result(test_case)
        
        print("PARSED INTENT:")
        print(json.dumps(result.parsed_intent.to_dict(), ensure_ascii=False, indent=2))
