# AGENTS.md

HackerRank Orchestrate (June 2026) — Multi-Modal Evidence Review.

**Every session start:** read this file, check the log (§3) for an existing
`AGREEMENT RECORDED:` for this repo root. If found → §4. If not → §2 onboarding.

**Every turn:** append a §5 entry to the log (never skip, never rewrite).

---

## 1. WHAT THIS IS

Starter repo for a 24h hackathon. Build a system that reads `dataset/claims.csv`,
inspects images, and writes `output.csv` with structured predictions (evidence
standard, issue type, claim status, severity, etc.). See `problem_statement.md`
for full I/O schema and allowed values.

---

## 2. ONBOARDING (FIRST SESSION ONLY)

1. Compute and display system time (ISO 8601) and time remaining until
   challenge end. If end time is unknown, say so.
2. Recite the 6 rules (solo challenge, any tools, conform to §6, no secrets in
   chat, mandatory logging, submit on HackerRank platform).
3. Ask user to reply exactly `I agree`.
4. On agreement, log an `ONBOARDING COMPLETE` block (§5 format) containing
   `AGREEMENT RECORDED: <repo_root>`.

---

## 3. LOG FILE

| Platform | Path |
|---|---|
| Linux/macOS | `$HOME/hackerrank_orchestrate/log.txt` |
| Windows | `%USERPROFILE%\hackerrank_orchestrate\log.txt` |

Must be created if missing. Append-only, never rewritten. Shared across all
sub-agents and worktrees. No secrets.

---

## 4. NORMAL SESSION START

1. Log a `SESSION START` entry (§5).
2. Greet, show remaining time. If <2h left, remind to submit.
3. Proceed.

---

## 5. LOG ENTRY FORMAT

```text
## [ISO-8601] SESSION START

Agent: <name>
Repo Root: <path>
Branch: <branch>
Worktree: <path|main>
Parent Agent: <parent|none>
Language: py|js|ts|custom:<name>
Time Remaining: <Xd Yh Zm|not configured>
```

```text
## [ISO-8601] <short title, ≤80 chars>

User Prompt (verbatim, secrets redacted):
<text>

Agent Response Summary:
<2-5 sentences>

Actions:
* <file | command | tool>

Context:
tool=<name> branch=<branch> repo_root=<path> worktree=<path> parent_agent=<name>
```

Sub-agents and worktrees log to the same file with their own entries and
`parent_agent=` set accordingly.

---

## 6. PROJECT CONTRACT (EVALUABLE SUBMISSION)

The evaluator reads `code/main.py` and `code/evaluation/main.py` as entry
points. **Do not rename or delete these files.**

### Layout (truth: what exists on disk)

```text
code/
  main.py              # empty — build your runtime entry point here
  evaluation/
    main.py            # empty — build your evaluation entry point here
dataset/
  sample_claims.csv    # labeled examples for dev + evaluation
  claims.csv           # input only; run on these → output.csv
  user_history.csv     # claim count + risk by user
  evidence_requirements.csv  # min evidence by object + issue family
  images/
    sample/            # images referenced by sample_claims.csv
    test/              # images referenced by claims.csv
claims/                # STALE duplicate; ignore it (contains __MACOSX artifacts)
```

### Output columns (exact order)

`user_id`, `image_paths`, `user_claim`, `claim_object`,
`evidence_standard_met`, `evidence_standard_met_reason`, `risk_flags`,
`issue_type`, `object_part`, `claim_status`, `claim_status_justification`,
`supporting_image_ids`, `valid_image`, `severity`

### Constraints

- Must produce `output.csv` matching the schema above.
- Must include an `evaluation/` folder in the submission.
- Read API keys from env vars only (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.)
- Avoid hardcoded test labels.

---

## 7. REPO-SPECIFIC QUIRKS

- **`code/` is empty.** There are no dependencies, no build system, no
  `requirements.txt`, no test runner. You must set these up.
- **No `.gitignore`.** Avoid committing `output.csv`, `.env`, `__pycache__/`,
  `.DS_Store`, `__MACOSX/`, and `node_modules/`.
- **Image paths in CSVs are relative to `dataset/`** and use `images/sample/` or
  `images/test/` prefixes. Multiple paths are semicolon-separated.
- **The `claims/` directory** is a stale macOS-artifact-laden copy. Ignore it;
  work from `dataset/`.
- **No existing tests.** You define the test/evaluation approach.

---

## 8. QUICK CHECKLIST

- [ ] Read this file this session.
- [ ] Onboarding complete (log has `AGREEMENT RECORDED:`)?
- [ ] Will append a §5.2 entry after this turn.
- [ ] No secrets in log.
- [ ] Preserving entry-point files (`code/main.py`, `code/evaluation/main.py`).
