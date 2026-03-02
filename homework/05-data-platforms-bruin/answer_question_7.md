# Question 7

## Task Explanation

When running a pipeline for the first time on a new database, tables need to be created from scratch. This question asks for the correct flag.

### Query Function

**Command (bash):**
```bash
bruin run . --full-refresh
```

**Breakdown:**
1.  **`bruin run .`**: Run the entire pipeline
2.  **`--full-refresh`**: Flag to create/replace tables from scratch

**Multiple Choice Options:**
- `--create`
- `--init`
- `--full-refresh`
- `--truncate`

**Answer:** **`--full-refresh`**

**Reason:**
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
