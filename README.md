# natural-language-execution-brain-1.0.0

**A skill that translates messy natural language into executable agent action.**

---

## Quick Start

### What It Does

When a user gives vague, emotional, incomplete, or indirect instructions, this skill:

1. Extracts the real intent (not just literal wording)
2. Identifies constraints and boundaries
3. Infers hidden priorities
4. Produces an executable action plan
5. Eliminates unnecessary back-and-forth

### How to Use

```python
from src.interpreter import NaturalLanguageExecutionBrain
import json

brain = NaturalLanguageExecutionBrain()

user_text = "你直接做，除了付款和法律，别问我。"

parsed = brain.parse_user_intent(user_text)

# Returns structured intent with:
# - real_goal
# - deliverable
# - hard_constraints
# - approval_boundaries
# - execution_mode
# - next_actions
# - ... and more
```

---

## Core Concept

**Humans describe outcomes. Agents must translate outcomes into actions.**

| What User Says | What User Means | What Agent Does |
|---|---|---|
| "不要问我" | Maximize autonomous execution | Set `execution_mode: autonomous_execute` |
| "方向不对" | Current work is misaligned | Pause, re-anchor to real goal |
| "别分析，直接给我能用的" | Operational output, not explanation | Output executable instructions |
| "除非付款，不要找我" | Gate only on payment approval | `approval_boundaries: ["payment"]` |

---

## File Structure

```
natural-language-execution-brain-1.0.0/
├── SKILL.md                 # Full specification & doctrine
├── README.md                # This file (quick start)
├── src/
│   ├── interpreter.py       # Main NaturalLanguageExecutionBrain class
│   ├── intent_parser.py     # Intent parsing logic
│   ├── constraint_extractor.py
│   ├── ambiguity_resolver.py
│   ├── action_translator.py
│   ├── approval_guard.py
│   ├── execution_brief.py
│   ├── schema.py            # Data structures
│   └── utils.py
├── templates/
│   ├── intent_parse.template.json
│   ├── execution_brief.template.json
│   └── action_plan.template.json
└── examples/
    ├── vague_user_request.json
    ├── frustrated_user_request.json
    └── autonomy_boundary_request.json
```

---

## Key Classes & Functions

### `NaturalLanguageExecutionBrain`

Main class that parses user intent.

**Method:** `parse_user_intent(user_text: str) -> IntentParse`

Returns a structured intent with all extracted fields.

### `IntentParse` (Dataclass)

Structured representation of parsed intent.

Fields:
- `intent_summary` — What user really wants
- `real_goal` — Actual intended outcome
- `deliverable` — Concrete output
- `hard_constraints` — Non-negotiable rules
- `soft_preferences` — Preferred style
- `forbidden_actions` — What not to do
- `approval_boundaries` — Escalation gates
- `assumptions` — Inferred context
- `execution_mode` — How to proceed
- `urgency` — Speed expectation
- `next_actions` — Ordered tasks
- `success_criteria` — Definition of done
- `fallback_plan` — If blocked

---

## Supported Execution Modes

| Mode | Use Case |
|------|----------|
| `direct_execute` | Immediate output (default) |
| `autonomous_execute` | User wants independent action |
| `analyze_then_execute` | Analysis needed before action |
| `draft_then_execute` | Show draft first, then execute |
| `approval_gated_execute` | Gate specific items (e.g., payment, legal) |
| `monitor_only` | Report status without action |

---

## Example Workflows

### Example 1: Vague Request

**User:** "你给我写一个skill，提升agent理解能力。我放到VS Code里面。"

**Parsed Intent:**
```json
{
  "intent_summary": "User wants a reusable skill to improve agent understanding",
  "real_goal": "Enhance agent's ability to interpret ambiguous language accurately",
  "deliverable": "Production-usable skill with full implementation",
  "execution_mode": "direct_execute",
  "next_actions": [
    "Create skill directory structure",
    "Write SKILL.md specification",
    "Implement core Python modules",
    "Add templates and examples"
  ]
}
```

**Agent Action:** Create the skill immediately.

---

### Example 2: Frustrated Request

**User:** "别老汇报，直接推进。除非付款和法律，不要来问我。"

**Parsed Intent:**
```json
{
  "intent_summary": "User wants autonomous execution with minimal communication",
  "real_goal": "Maximize independent agent work",
  "hard_constraints": [
    "Minimize status reporting",
    "Gate only on payment and legal"
  ],
  "forbidden_actions": [
    "Unnecessary check-ins",
    "Asking permission on routine tasks"
  ],
  "execution_mode": "autonomous_execute",
  "approval_boundaries": ["payment", "legal"]
}
```

**Agent Action:** Operate independently. Only escalate payment and legal decisions. Don't report status unless there's a blocker.

---

### Example 3: Specification Request

**User:** "你别分析，直接给我能发给团队执行的东西。"

**Parsed Intent:**
```json
{
  "intent_summary": "User wants operational instructions, not analysis",
  "real_goal": "Get a ready-to-paste execution prompt",
  "deliverable": "Operational instruction block for team execution",
  "forbidden_actions": [
    "Abstract analysis",
    "Explanation of reasoning"
  ],
  "execution_mode": "direct_execute",
  "style": "concise, actionable"
}
```

**Agent Action:** Output executable instructions directly. Skip explanation.

---

## Configuration

The skill works out of the box. Optional customization:

### Add Custom Approval Keywords

```python
brain = NaturalLanguageExecutionBrain()
brain.approval_keywords.extend(["security", "compliance"])
```

### Add Custom Autonomy Patterns

```python
brain.autonomy_keywords.extend(["no check-ins", "hands-off"])
```

---

## Testing

Run the test examples:

```bash
python src/interpreter.py
```

This executes sample intents and prints parsed results as JSON.

---

## Design Philosophy

This skill is built on these principles:

1. **Preserve Intent, Not Wording** — Translate meaning, not repeat words
2. **Infer Before Asking** — Reduce back-and-forth through smart inference
3. **Act Before Explaining** — Move work forward instead of discussing
4. **Emotional Language is Data** — Treat frustration, urgency as operational signals
5. **Ambiguity is Solvable** — Only freeze at true blockers (approval, safety, access)
6. **Success = Alignment** — Measure success by action quality, not tone

---

## When to Use This Skill

Use it when:
- User language is vague or indirect
- Intent and literal wording diverge
- Minimizing back-and-forth is important
- The agent needs autonomous action boundaries
- Emotional or frustrated language appears
- User expects the agent to "just understand"

---

## Next Steps

1. **Read SKILL.md** for full specification and interpretation doctrine
2. **Explore templates/** for JSON structure examples
3. **Check examples/** for real-world parsing scenarios
4. **Integrate into your agent** by calling `parse_user_intent()` early in message processing
5. **Customize keywords** for your domain

---

## Version

**1.0.0** — Initial release

Core capabilities:
- Intent parsing from natural language
- Constraint extraction
- Approval boundary detection
- Execution mode inference
- Action plan generation
- Ambiguity resolution

---

## License

Use freely in your agent systems.

---

## Support

For questions or improvements, refer to SKILL.md for detailed interpretation doctrine and integration patterns.
