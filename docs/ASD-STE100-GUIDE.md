# Why ASD-STE100 for AI Agent Skills?

**ASD-STE100 (Simplified Technical English)** was created by the aerospace and defense industry so technicians never misread maintenance instructions.

An LLM agent reading a `SKILL.md` file or an inter-agent handoff faces the exact same risk: there is no human author in the loop to clarify ambiguous pronouns, passive actors, or synonym rotation.

## Enforced Structural Rules in This Repository

1. **Sentence Length Caps**: `<= 20` words for procedural steps, `<= 25` words for descriptive sentences.
2. **One Instruction Per Sentence**: Prevents skipped steps and compound-clause confusion.
3. **Active Voice & Imperative Mood**: Makes the actor and action explicit.
4. **Condition-First Ordering**: `If X occurs, do Y.` ensures agents evaluate preconditions before acting.
5. **No Semicolons (`;`) or Em/En-Dashes**: Forces clean sentence boundaries.
6. **Noun Clusters `<= 3` Words**: Eliminates modifier attachment ambiguity.
7. **One Term Per Concept**: Prevents synonym drift across prompts.
