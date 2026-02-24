# Question 3: Pipeline Variables

## Task Explanation

Pipeline variables are used to parameterize pipelines. This question asks how to override the `taxi_types` variable during runtime to only process yellow taxis.

## Query Function

**Variable Definition (pipeline.yml):**
```yaml
variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
```

**Override Command:**
```bash
bruin run . --var 'taxi_types=["yellow"]'
```

**Breakdown:**
1. **`--var`**: Flag to override variable
2. **`'taxi_types=["yellow"]'`**: JSON array format as string value

## Multiple Choice Options

- `bruin run --taxi-types yellow`
- `bruin run --var taxi_types=yellow`
- `bruin run --var 'taxi_types=["yellow"]'`
- `bruin run --set taxi_types=["yellow"]`

## Answer

**`bruin run --var 'taxi_types=["yellow"]'`**

## Reason

- The correct format is `--var 'key=value'`
- Value must be in JSON format since `taxi_types` is defined as an array
- Single quotes are required so the shell doesn't interpret brackets

**Usage in Assets:**

SQL:
```sql
WHERE taxi_type IN {{ var.taxi_types }}
```

Python:
```python
import os, json
vars = json.loads(os.environ.get("BRUIN_VARS", "{}"))
taxi_types = vars.get("taxi_types", [])
```
