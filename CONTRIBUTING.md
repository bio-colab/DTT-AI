# Contributing

Thank you for contributing to the **Digital Thinking Tools AI Skills Suite**.

## Requirements for New or Updated Skills

1. **Kebab-case Naming**: Place each skill under `skills/<kebab-case-name>/SKILL.md` with matching `name` in YAML frontmatter.
2. **ASD-STE100 Compliance**: Every `SKILL.md` must pass `ste100_linter.py` with **0 errors**:
   - Procedural steps: `<= 20` words per sentence.
   - Descriptive prose: `<= 25` words per sentence.
   - Active voice, imperative mood, one instruction per sentence.
   - Zero semicolons (`;`), em-dashes, or en-dashes.
3. **Tests**: Add unit tests under `tests/` for any new deterministic script.

## Local Verification

```bash
python3 skills/asd-ste100-skill-linter/scripts/ste100_linter.py skills/
python3 -m unittest discover -s tests -v
```
