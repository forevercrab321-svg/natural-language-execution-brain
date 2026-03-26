"""Intent parser module for natural language to intent conversion."""

from typing import List
from src.schema import IntentParse
from src import utils


class IntentParser:
    """Parses natural language into structured intent."""
    
    def __init__(self):
        self.approval_keywords = [
            "付款", "收款", "支付", "合同", "legal", "law", "法律", "发票",
            "payment", "contract", "agreement", "sign"
        ]
        self.autonomy_keywords = [
            "直接做", "别问我", "自己解决", "自动推进", "自行操作",
            "autonomous", "independent", "hands-off", "don't ask"
        ]
        self.no_analysis_keywords = [
            "别分析", "不要分析", "直接给我", "不要讲过程", "我要结果",
            "no analysis", "just give me", "results only"
        ]
        self.frustration_keywords = [
            "方向不对", "没理解", "不是这个意思", "跑偏了", "你没听懂",
            "wrong direction", "misunderstood", "off track"
        ]
        self.skill_keywords = [
            "skill", "技能", "能力", "功能", "feature"
        ]

    def build_intent_summary(self, text: str) -> str:
        """Build a concise summary of what the user really wants."""
        if utils.contains_any_keyword(text, self.frustration_keywords):
            return "User believes current execution is misaligned and wants rapid re-anchoring toward real goal."
        
        if utils.contains_any_keyword(text, self.no_analysis_keywords):
            return "User wants operational output, not abstract analysis."
        
        if utils.contains_any_keyword(text, self.autonomy_keywords):
            return "User wants autonomous execution with minimal back-and-forth."
        
        if utils.contains_any_keyword(text, self.skill_keywords):
            return "User wants to create or improve a reusable agent capability."
        
        return "User provided natural-language instruction requiring translation to executable action."

    def infer_real_goal(self, text: str) -> str:
        """Infer the actual intended outcome."""
        patterns = [
            (r"提示词|prompt", "Obtain a ready-to-use operational prompt that can be pasted directly."),
            (r"skill|SKILL|技能|能力", "Create or improve a reusable skill that enhances agent capability."),
            (r"理解|听懂|准确|parsing", "Improve semantic understanding so agent correctly interprets language into action."),
            (r"剪辑|edit|video", "Build automatic editing capability with professional judgment."),
            (r"自动|auto", "Automate a process that currently requires manual intervention."),
        ]
        
        for pattern, goal in patterns:
            if utils.find_pattern_matches(text, pattern):
                return goal
        
        return "Translate natural language into the most likely intended executable outcome."

    def infer_deliverable(self, text: str) -> str:
        """Infer what concrete output the user expects."""
        if utils.contains_any_keyword(text, self.skill_keywords):
            return "Production-usable skill with full specification, code, and examples."
        
        if utils.contains_any_keyword(text, ["提示词", "prompt"]):
            return "Ready-to-paste operational instruction block."
        
        if utils.contains_any_keyword(text, ["代码", "code", "implement"]):
            return "Starter code that can be integrated into the project."
        
        if utils.contains_any_keyword(text, ["分析", "analyze", "explain"]):
            return "Clear analysis with actionable conclusions."
        
        return "Actionable output matching the user's actual execution need."

    def extract_hard_constraints(self, text: str) -> List[str]:
        """Extract non-negotiable rules and constraints."""
        constraints = []
        
        if utils.contains_any_keyword(text, ["不要问我", "别问我", "别汇报", "不要汇报"]):
            constraints.append("Minimize clarification questions and status reports.")
        
        if "除非" in text and utils.contains_any_keyword(text, self.approval_keywords):
            approval_kws = utils.detect_approval_keywords_in_text(text, self.approval_keywords)
            constraints.append(f"Only escalate for approval on: {', '.join(approval_kws)}")
        
        if utils.contains_any_keyword(text, ["直接", "马上", "立刻"]):
            constraints.append("Prefer immediate actionable output over extensive planning.")
        
        if utils.contains_any_keyword(text, ["别老", "停止", "不再"]):
            constraints.append("Disable passive assistant behavior.")
        
        return constraints

    def extract_soft_preferences(self, text: str) -> List[str]:
        """Extract preferred style and direction."""
        prefs = []
        
        if utils.contains_any_keyword(text, ["顶级", "最好", "高质量", "professional"]):
            prefs.append("High-quality, professional-grade output.")
        
        if utils.contains_any_keyword(text, ["简洁", "直接", "concise"]):
            prefs.append("Concise, operational style (avoid verbosity).")
        
        if utils.contains_any_keyword(text, ["详细", "详尽", "comprehensive"]):
            prefs.append("Comprehensive, well-documented output.")
        
        if utils.contains_any_keyword(text, ["VS Code", "vscode", "editor"]):
            prefs.append("Output should be copy-paste friendly for local development.")
        
        if utils.contains_any_keyword(text, ["能发给团队", "给团队", "team"]):
            prefs.append("Output should be shareable with team members.")
        
        return prefs

    def extract_forbidden_actions(self, text: str) -> List[str]:
        """Extract explicitly or implicitly forbidden actions."""
        forbidden = []
        
        if utils.contains_any_keyword(text, self.no_analysis_keywords):
            forbidden.append("Do not respond with abstract analysis; provide executable output.")
        
        if utils.contains_any_keyword(text, ["别老汇报", "不要汇报", "no status"]):
            forbidden.append("Do not produce unnecessary status reports.")
        
        if utils.contains_any_keyword(text, ["不要教程", "no tutorial"]):
            forbidden.append("Do not give tutorial-style output.")
        
        if utils.contains_any_keyword(text, ["不要列表", "别列举"]):
            forbidden.append("Do not list options; choose a direction.")
        
        return forbidden

    def detect_approval_boundaries(self, text: str) -> List[str]:
        """Detect approval gates and boundaries."""
        found_keywords = utils.detect_approval_keywords_in_text(text, self.approval_keywords)
        
        seen = set()
        result = []
        for b in found_keywords:
            if b not in seen:
                seen.add(b)
                result.append(b)
        
        return result

    def resolve_assumptions(self, text: str) -> List[str]:
        """Identify and record assumptions made during parsing."""
        assumptions = []
        
        if utils.contains_any_keyword(text, self.skill_keywords):
            assumptions.append("User wants reusable skill files, not one-time advice.")
        
        if utils.contains_any_keyword(text, ["放到", "VS Code", "project"]):
            assumptions.append("Output should be directly usable as local project content.")
        
        if utils.contains_any_keyword(text, ["理解", "自然语言", "parsing"]):
            assumptions.append("User wants stronger intent parsing capability, not just better wording.")
        
        if utils.contains_any_keyword(text, ["顶级", "高质量"]):
            assumptions.append("Quality and completeness are important; avoid shortcuts.")
        
        if len(utils.detect_approval_keywords_in_text(text, self.approval_keywords)) == 0 and \
           utils.contains_any_keyword(text, ["别问我", "自己做"]):
            assumptions.append("Approval gate exists only for explicitly mentioned items.")
        
        return assumptions

    def infer_execution_mode(self, text: str) -> str:
        """Infer the correct execution mode from user language."""
        if utils.contains_any_keyword(text, self.autonomy_keywords):
            return "autonomous_execute"
        
        if utils.contains_any_keyword(text, ["先分析", "analyze first"]):
            return "analyze_then_execute"
        
        if utils.contains_any_keyword(text, ["给我一段", "给我代码", "draft"]):
            return "draft_then_execute"
        
        if utils.contains_any_keyword(text, ["除非", "only"]) and \
           len(utils.detect_approval_keywords_in_text(text, self.approval_keywords)) > 0:
            return "approval_gated_execute"
        
        return "direct_execute"

    def infer_urgency(self, text: str) -> str:
        """Infer urgency level."""
        if utils.contains_any_keyword(text, ["立刻", "马上", "现在", "urgent", "asap"]):
            return "high"
        
        if utils.contains_any_keyword(text, ["稍后", "later", "deferred"]):
            return "deferred"
        
        return "normal"

    def translate_to_actions(self, text: str, real_goal: str, deliverable: str) -> List[str]:
        """Translate intent into ordered actionable tasks."""
        actions = [
            f"Verify goal alignment: {real_goal[:50]}...",
            f"Prepare deliverable: {deliverable[:50]}...",
            "Extract execution constraints and boundaries.",
            "Convert natural language into ordered actionable tasks.",
        ]
        
        if utils.contains_any_keyword(text, self.skill_keywords):
            actions.extend([
                "Create skill directory structure and file organization.",
                "Write comprehensive skill specification document.",
                "Implement core Python modules with proper structure.",
                "Add templates and example usage scenarios.",
                "Test all modules with sample inputs.",
            ])
        
        if utils.contains_any_keyword(text, ["提示词", "prompt"]):
            actions.append("Format as ready-to-paste prompt block.")
        
        if utils.contains_any_keyword(text, ["代码", "code"]):
            actions.append("Write production-quality starter code.")
        
        return actions

    def build_success_criteria(self, real_goal: str, deliverable: str) -> List[str]:
        """Define what successful execution looks like."""
        return [
            f"Output advances the real goal: {real_goal[:60]}...",
            f"Deliverable is concrete and usable: {deliverable[:60]}...",
            "Result can be used immediately without heavy reworking.",
            "Ambiguity is resolved, not repeated.",
            "Constraints are respected.",
        ]

    def build_fallback_plan(self, text: str) -> List[str]:
        """Define fallback steps if primary approach is blocked."""
        return [
            "If intent remains ambiguous, choose the most execution-friendly interpretation.",
            "If an approval boundary appears, isolate only that portion for escalation.",
            "If constraints conflict, prioritize explicit hard constraints over preferences.",
            "If blocked on input, infer the most likely missing information.",
        ]
