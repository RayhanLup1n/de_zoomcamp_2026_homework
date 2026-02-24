# Question 6: Lineage and Dependencies

## Task Explanation

Lineage visualizes the dependency graph between assets. This question asks which command to use to view it.

## Query Function

**Command:**
```bash
bruin lineage assets/ingestion/trips.py
```

**Breakdown:**
1. **`bruin lineage`**: Command to view dependency graph
2. **`assets/ingestion/trips.py`**: Path to asset to view lineage for

**Example Output:**
```
UPSTREAM:
  - ingestion.payment_lookup

DOWNSTREAM:
  - staging.trips
  - reports.trips_report
```

## Multiple Choice Options

- `bruin graph`
- `bruin dependencies`
- `bruin lineage`
- `bruin show`

## Answer

**`bruin lineage`**

## Reason

- `bruin lineage` is the official command to view dependency graph
- Shows upstream (dependencies) and downstream (dependents)

The command `bruin lineage <path>` displays:
- **Upstream dependencies** - what this asset depends on
- **Downstream dependencies** - what depends on this asset
