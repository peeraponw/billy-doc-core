# 13. Git Workflow and Search Commands

## 13.1 Branching

* Branch names MUST follow:

  * `main` — production-ready
  * `dev` — integration
  * `feat/*` — features
  * `fix/*` — bug fixes
  * `docs/*` — documentation
  * `refactor/*` — refactors
  * `test/*` — test-specific changes

## 13.2 Commit Messages

* Commits MUST follow a semantic style:

```text
feat(auth): add jwt-based login
fix(api): handle invalid pagination params
docs(readme): update setup instructions
```

## 13.3 Search Commands

* `rg` (ripgrep) MUST be used for searching.
* `grep` and `find` MUST NOT be used in scripts or documented workflows.

```bash
rg "pattern"
rg --files -g "*.py"
```
