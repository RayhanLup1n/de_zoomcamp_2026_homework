# Question 1

## Task Explanation

In a Bruin project, certain files and directories are required for the pipeline to function correctly. This question asks about the **required** components of a Bruin project.

### Query Function

**Config (YAML):**
```yaml
# .bruin.yml - Environment & connections (in root directory)
# pipeline.yml - Pipeline configuration (in pipeline/ or root)
# assets/ - Asset files (SQL, Python, YAML)
```

**Breakdown:**
1.  **`.bruin.yml`**: Stores environment configuration (dev, staging, prod) and connections to databases/APIs. Must exist in root directory and should be **gitignored**.
2.  **`pipeline.yml`**: Stores pipeline configuration including name, schedule, start_date, default_connections, and variables.
3.  **`assets/`**: Folder containing asset files. Can be placed anywhere as long as detected by git.

**Multiple Choice Options:**
- `bruin.yml` and `assets/`
- `.bruin.yml` and `pipeline.yml` (assets can be anywhere)
- `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`
- `pipeline.yml` and `assets/` only

**Answer:** **`.bruin.yml` and `pipeline.yml` (assets can be anywhere)**

**Reason:**
- `.bruin.yml` is required in root for environment & connections
- `pipeline.yml` is required for pipeline configuration
- `assets/` can be placed anywhere (default: next to `pipeline.yml`)
