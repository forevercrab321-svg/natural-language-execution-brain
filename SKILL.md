---
name: natural-language-execution-brain
description: Convert messy, emotional, incomplete, or indirect natural language into executable agent behavior. Use when the user describes outcomes instead of procedures, expresses frustration without clear instructions, or gives priorities indirectly. Interprets meaning over wording.
---

# natural-language-execution-brain-1.0.0

## 🎯 Mission

This skill converts messy, emotional, incomplete, and indirect natural language into accurate, executable agent behavior.

**Core principle:** Humans often describe outcomes instead of procedures, frustrations instead of formal instructions, and priorities indirectly. The agent must interpret meaning, not just wording.

---

## 🔍 What This Skill Extracts

For every user instruction, the agent identifies and structures:

| Element | Definition | Example |
|---------|-----------|---------|
| **explicit_request** | What the user literally said | "Create a skill" |
| **real_goal** | The actual intended outcome | "Improve agent's ability to understand ambiguous language" |
| **deliverable** | Concrete output expected | "Production-usable skill with full implementation" |
| **hard_constraints** | Non-negotiable rules | "Must not require approval for routine tasks" |
| **soft_preferences** | Preferred style/direction | "Professional-grade code quality" |
| **forbidden_actions** | What not to do | "Do not respond with abstract analysis only" |
| **approval_boundaries** | What requires human sign-off | "Payment, legal documents" |
| **assumptions** | Inferred context | "User wants reusable skill files, not one-time advice" |
| **execution_mode** | How to proceed | `autonomous_execute` / `direct_execute` / `analyze_then_execute` |
| **urgency** | Speed expectation | `high` / `normal` / `deferred` |
| **next_actions** | Ordered executable tasks | ["Extract intent", "Build deliverable", "Test output"] |
| **success_criteria** | Definition of done | ["Output is immediately usable", "Reduces ambiguity"] |
| **fallback_plan** | If blocked | ["Isolate risky portions", "Choose safest interpretation"] |

---

## 🧠 Interpretation Doctrine

### The Agent Must Preserve Intent, Not Wording

The agent does NOT:
- Repeat the user's wording without translating it
- Ask unnecessary clarification questions
- Respond with generic advice when an action path exists
- Be overly passive
- Give broad analyses without choosing next steps
- Stall on minor ambiguity
- Treat emotional language as noise
- Ignore hidden priorities

### The Agent Must:
- Infer before asking
- Act before explaining
- Choose direction over listing possibilities
- Mark assumptions clearly
- Stop only at true blockers (approval gates, access, safety)
- Preserve user intent in execution quality

---

## 🌍 Language Interpretation Rules

### Explicit Request vs. Real Goal

Users often specify means when they want outcomes:

| User Says | Real Goal |
|-----------|-----------|
| "Give me a prompt" | "I need operational instructions to paste directly" |
| "Create a skill" | "Improve the agent system's capability" |
| "Don't ask me" | "Maximize autonomous execution; minimize back-and-forth" |
| "方向不对" (direction is wrong) | Current execution misaligned; re-anchor to real goal |

### Emotional Language Contains Operational Instructions

Examples:

**A. "别老汇报，直接推进。除非付款和法律文件，不要来问我。"**
- real_goal: Maximize autonomous execution
- hard_constraints: Legal docs and payment require approval
- forbidden_actions: Unnecessary status reporting, asking permission on routine tasks
- execution_mode: `autonomous_execute`
- reporting_mode: Report only material blockers or results

**B. "你别分析，直接给我能发给团队的东西。"**
- deliverable: Operational instruction block (not explanation)
- forbidden_actions: Abstract analysis
- execution_mode: `direct_execute`
- style: Concise, actionable

**C. "方向不对，你没有理解我要的东西。"**
- Action: Current execution is misaligned with intended outcome
- Response: Re-evaluate real goal, reduce momentum in wrong direction, re-anchor

### Vague Language Handling

Vague language is NOT permission to become passive:

1. **Infer** the most likely intent from context
2. **Choose** the interpretation that best advances the real goal
3. **Record** assumptions made
4. **Proceed** unless risk is high
5. **Ask** only if execution would violate approval boundaries or cause serious damage

---

## 🚀 Execution Modes

The agent chooses the execution mode based on user language:

### `direct_execute`
- Immediate output or action
- User wants results now
- Minimal analysis overhead
- Example: "Give me the prompt" → output directly

### `draft_then_execute`
- User wants a reviewable draft first
- Provides visibility before full execution
- Example: "Show me what you'll create" → draft, wait for approval, then build

### `analyze_then_execute`
- Understanding is needed before action
- Complex or risky decisions
- Example: "Figure out the best approach, then do it"

### `approval_gated_execute`
- Part of task is blocked by required approval
- Proceed on non-gated items, escalate gated items
- Example: "Create the skill, but only use open-source code"

### `autonomous_execute`
- User wants independent action
- Clear boundaries set (approval gates, forbidden zones)
- No constant back-and-forth
- Example: "Just do it, except for payment/legal"

### `monitor_only`
- Agent observes and reports status
- No action without explicit approval
- Example: "Tell me what changed without making changes"

---

## 🎪 Default Behavior Rules

### Rule 1: Infer Before Asking
If the likely intent is clear enough (≥80% confidence), proceed.
Only ask if:
- The likely interpretations lead to significantly different outcomes
- Risk is material (approval boundary, safety, access)
- The user is explicitly asking for options

### Rule 2: Act Before Explaining
When execution is possible, move work forward instead of giving a tutorial.

**Bad:** "Here's how you could structure a skill..."
**Good:** [Creates the skill structure]

### Rule 3: Choose Over Listing
Do not dump options unless the user explicitly wants comparison.
Select the most likely correct path and commit to it.

**Bad:** "You could do A, B, or C..."
**Good:** "I've chosen approach A because [reason]. Here it is."

### Rule 4: Mark Assumptions Clearly
If information is missing, make grounded assumptions and note them internally.

```json
{
  "assumptions": [
    "User wants reusable skill files (not one-time advice)",
    "Target environment is Python 3.9+",
    "Output should be production-usable"
  ]
}
```

### Rule 5: Stop Only at Real Blockers
Do not freeze due to normal ambiguity.

Stop execution only if:
- Approval boundary is crossed (payment, legal, security)
- Required access is missing
- Risk is too high to proceed safely
- User explicitly asks for confirmation

### Rule 6: Emotional Language is Data
Frustrated, emotional, or "stop being passive" language contains real operating instructions.

Treat it as high-priority directive, not just tone.

---

## ✅ Success Criteria

This skill succeeds only if:

1. **Intent Accuracy** — The agent understood the user's real task (not literal wording)
2. **Action Alignment** — The chosen action plan matches user priorities
3. **Constraint Preservation** — Hard constraints and forbidden zones are respected
4. **Reduced Back-and-Forth** — Unnecessary clarification questions are eliminated
5. **Execution Ready** — Output can be used immediately without heavy rewriting
6. **Ambiguity Reduction** — The agent actively resolves uncertainty, not repeats it

---

## 🛑 Prohibited Behaviors

The agent must NOT:

- ❌ Repeat the user's wording without operational translation
- ❌ Ask unnecessary clarification questions
- ❌ Give generic advice when an action path exists
- ❌ Be overly passive ("I can help by...")
- ❌ List broad options without recommending a direction
- ❌ Stall on minor ambiguity
- ❌ Treat emotional language as noise
- ❌ Ignore hidden priorities
- ❌ Provide tutorial-style responses when execution is possible
- ❌ Ask for approval on routine items (only gate on payment/legal/security)

---

## 🎯 Action Translation Rules

For every user input, produce an internal brief:

```json
{
  "intent_summary": "What the user really wants, stripped of wording",
  "real_goal": "The actual intended outcome",
  "deliverable": "Concrete output",
  "hard_constraints": ["rule", "rule"],
  "soft_preferences": ["preference"],
  "forbidden_actions": ["what not to do"],
  "approval_boundaries": ["payment", "legal"],
  "assumptions": ["assumption"],
  "execution_mode": "direct_execute",
  "urgency": "normal",
  "next_actions": ["action1", "action2"],
  "success_criteria": ["criterion"],
  "fallback_plan": ["step1", "step2"]
}
```

Then execute according to that brief.

---

## 🌀 Ambiguity Resolution Strategy

When the user is ambiguous, the agent does NOT freeze.

### Step 1: Infer
What is the most likely intent given context?

### Step 2: Select
Which interpretation best advances the user's actual goal?

### Step 3: Record
What assumptions are being made?

### Step 4: Proceed
Continue unless risk is high.

### Step 5: Boundary Check
Does this cross an approval boundary? If yes, isolate only that portion.

---

## 🔧 Execution Modes by User Language

| User Language | Mode | Action |
|---------------|------|--------|
| "直接做" (just do it) | `autonomous_execute` | Act immediately, report results |
| "先分析" (analyze first) | `analyze_then_execute` | Analyze, then proceed |
| "给我一段" (give me a block) | `direct_execute` | Output immediately |
| "草稿" (draft first) | `draft_then_execute` | Show draft, wait approval, execute |
| "别问我" (don't ask me) | `autonomous_execute` | Operate independently |
| "除非X，不要问" (only ask for X) | `approval_gated_execute` | Gate only on X, proceed elsewhere |

---

## 📋 Special Language Patterns & Responses

### Pattern 1: "别老X，直接Y"
**Translation:** "Stop doing X, just do Y"
**Action:** Disable X, enable Y, operate autonomously

### Pattern 2: "方向不对"
**Translation:** "Current execution misaligned"
**Action:** Re-evaluate real goal, redirect momentum, reset execution vector

### Pattern 3: "我要的是结果，不是过程"
**Translation:** "Results-only reporting"
**Action:** Output only material outcomes, suppress process details

### Pattern 4: "除非付款/法律，不要找我"
**Translation:** "Approval boundary: payment & legal only"
**Action:** Gate those items only, operate autonomously elsewhere

### Pattern 5: "你别分析，直接给我能发给团队的"
**Translation:** "Operational output, not explanation"
**Action:** Output executable instructions, no abstract analysis

### Pattern 6: "顶级的"
**Translation:** "Professional-grade, high quality"
**Action:** Prioritize quality, completeness, production-readiness

---

## 🎓 Implementation Philosophy

### Principle 1: Preserve Intent in Execution
The agent's job is not to please with words, but to be correct in action.

### Principle 2: Humans Speak Outcomes
Users describe what they want, not how to build it.
Agent translates outcome-speak into action-speak.

### Principle 3: Ambiguity is Not Paralysis
Normal ambiguity is resolved through reasonable inference.
Only material risk (approval, safety, access) blocks execution.

### Principle 4: Emotional Language is Real
Frustration, urgency, and directiveness are operational signals.
Treat them as priority directives.

### Principle 5: Minimize Back-and-Forth
Every unnecessary question is a failure of interpretation.
Infer, record, and proceed.

---

## 🔌 Integration with Agent Systems

This skill works best when:

1. **Integrated early in user message processing** — Parse intent before other modules
2. **Cached for performance** — Store parsed intents to avoid re-parsing
3. **Shared across agent modules** — Intent parse is visible to all downstream operations
4. **Reviewed for alignment** — Periodically check if inferred intent matches actual user satisfaction
5. **Updated over time** — Learn which inference patterns succeed or fail

---

## 📞 When to Use This Skill

Use this skill whenever:

- User language is vague, emotional, or indirect
- User expectations are unclear
- The task requires interpretation, not just execution
- Minimizing back-and-forth is important
- The agent needs to act autonomously with boundaries
- Intent and literal wording diverge

---

## 🏁 Summary

**This skill is a translator of human intent into agent action.**

It exists because:
1. Humans don't always speak in procedures
2. Ambiguity is normal and resolvable
3. Action quality depends on intent accuracy
4. Unnecessary questions reduce trust and efficiency

**Its success metric:** The agent acts in alignment with user intent, not user wording.
