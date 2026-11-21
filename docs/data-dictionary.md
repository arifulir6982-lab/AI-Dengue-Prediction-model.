# Data dictionary & quality rules

- `date`: ISO-8601 period date; specify whether rows are daily or monthly and do not mix frequencies.
- `location`: canonical district/city identifier, not free-text variants where avoidable.
- `dengue_cases`: non-negative aggregate reported case count; document suspected vs confirmed/admitted case definition.
- `rainfall_mm`: precipitation accumulated over the same period, mm.
- `temperature_c`: period mean 2 m air temperature, °C.
- `humidity_pct`: period mean relative humidity, percent (0–100).

Quality controls:
- retain source URL, retrieval date, source version, license, transformation code and geographic mapping version;
- distinguish zero from missing, late report and unavailable;
- never silently convert missing case counts to zero;
- weather imputation must occur inside each training fold;
- retain population denominators and compute incidence per 100,000 when comparing regions;
- deduplicate by canonical location + period, and preserve source revisions.
