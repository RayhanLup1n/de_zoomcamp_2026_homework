# Question 7: First-Time Run

## Task Explanation

When running a pipeline for the first time on a new DuckDB database, you need to create tables from scratch. This question asks which flag to use.

## Query Function

**Command:**
```bash
bruin run . --full-refresh
```

**Breakdown:**
1. **`bruin run .`**: Run entire pipeline
2. **`--full-refresh`**: Flag to create/replace tables from scratch

## Multiple Choice Options

- `--create`
- `--init`
- `--full-refresh`
- `--truncate`

## Answer

**`--full-refresh`**

## Reason

- `--full-refresh` will truncate and rebuild tables from scratch
- Suitable for first-time run or when wanting to refresh all data

**Common Flags:**

| Flag | Purpose |
|------|---------|
| `--full-refresh` | Create/replace tables from scratch |
| `--only checks` | Run quality checks only |
| `--downstream` | Run asset + downstream |
| `--start-date` | Set start date for incremental run |
| `--end-date` | Set end date for incremental run |
| `--var` | Override variable |
