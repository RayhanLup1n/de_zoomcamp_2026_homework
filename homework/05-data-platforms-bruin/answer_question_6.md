# Question 6

## Task Explanation

Lineage visualizes the dependency graph between assets. This question asks which command to use to view it.

### Query Function

**Command (bash):**
```bash
bruin lineage assets/ingestion/trips.py
```

**Breakdown:**
1.  **`bruin lineage`**: Command to view dependency graph
2.  **`assets/ingestion/trips.py`**: Path to the asset

**Multiple Choice Options:**
- `bruin graph`
- `bruin dependencies`
- `bruin lineage`
- `bruin show`

**Answer:** **`bruin lineage`**

**Reason:**
- `bruin lineage` is the official command to view dependency graph
- Shows upstream (dependencies) and downstream (dependents)

**Example Output:**
```
UPSTREAM:
  - ingestion.payment_lookup

DOWNSTREAM:
  - staging.trips
  - reports.trips_report
```
