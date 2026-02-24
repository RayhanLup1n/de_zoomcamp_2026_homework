# Question 4: Running with Dependencies

## Task Explanation

After modifying `ingestion/trips.py`, you want to run it plus all downstream assets. This question asks for the correct command.

## Query Function

**Command:**
```bash
bruin run --select ingestion.trips+
```

**Breakdown:**
1. **`--select`**: Flag to select specific asset
2. **`ingestion.trips`**: Asset name (dot notation)
3. **`+`**: Include all downstream dependencies

**Dependency Graph Example:**
```
ingestion.payment_lookup
    ↓
ingestion.trips
    ↓
staging.trips
    ↓
reports.trips_report
```

## Multiple Choice Options

- `bruin run ingestion.trips --all`
- `bruin run ingestion/trips.py --downstream`
- `bruin run pipeline/trips.py --recursive`
- `bruin run --select ingestion.trips+`

## Answer

**`bruin run --select ingestion.trips+`**

## Reason

- `--select` with `+` notation is the official way to run asset + downstream
- `ingestion.trips` uses dot notation (asset path with dots)
- `+` means include all downstream dependencies

If you run `bruin run --select ingestion.trips+`, all assets from `ingestion.trips` downwards will be executed.

**Available Commands:**

| Command | Purpose |
|---------|---------|
| `bruin run <asset>` | Run single asset |
| `bruin run <asset> --downstream` | Run asset + downstream |
| `bruin run --select asset+` | Run asset + downstream (select syntax) |
| `bruin run --select asset+@<n>` | Run asset + n levels downstream |
