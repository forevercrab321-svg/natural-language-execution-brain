# Quick Start Guide

## What is This Skill?

A Python skill that automatically interprets messy, vague, or emotional natural language and converts it into structured, executable agent behavior.

## Install & Use

### Option 1: Direct Import
```python
from src.interpreter import NaturalLanguageExecutionBrain

brain = NaturalLanguageExecutionBrain()
parsed = brain.parse_user_intent("你直接做，除了付款别问我")
```

### Option 2: Full Pipeline
```python
result = brain.parse_full_result(user_text)
# Returns: intent, execution_brief, action_plan
```

## What You Get

```json
{
  "intent_summary": "What user really wants",
  "real_goal": "Actual outcome",
  "deliverable": "Concrete output",
  "hard_constraints": ["rules"],
  "execution_mode": "autonomous_execute",
  "approval_boundaries": ["payment"],
  "next_actions": ["steps"]
}
```

## Deploy to GitHub

```bash
# 1. Create repo at https://github.com/new

# 2. Run deployment:
bash ~/skills/natural-language-execution-brain-1.0.0/deploy-to-github.sh YOUR_USERNAME

# 3. Link: https://github.com/YOUR_USERNAME/natural-language-execution-brain
```

## Files to Know

- `SKILL.md` - Full specification & doctrine
- `README.md` - Detailed guide
- `src/interpreter.py` - Main entry point
- `examples/` - Real-world scenarios

## Key Features

✅ Parse vague language
✅ Infer hidden goals  
✅ Extract constraints
✅ Detect approval gates
✅ Choose execution mode
✅ Generate action plans

## Examples

See `examples/` directory for:
- Vague requests
- Frustrated users
- Autonomy boundaries

---

**Version**: 1.0.0
**Status**: Ready for production
