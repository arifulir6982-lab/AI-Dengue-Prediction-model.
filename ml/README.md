# Model training input

Expected CSV columns: `date, location, dengue_cases, rainfall_mm, temperature_c, humidity_pct`.

Use one regular frequency per location (weekly or monthly). The script resamples to monthly totals/means after sorting; for robust production work, build a separate panel per stable district ID and preserve reporting period semantics. Do not train on the bundled synthetic demo CSV. Missing cases are not imputed. Weather missing values are imputed inside the training pipeline. The current script uses lagged cases and lagged weather, month sine/cosine and a chronological 80/20 split. The residual interval is an empirical 90% absolute-residual interval on the held-out tail; it is a preliminary diagnostic, not guaranteed calibrated coverage. Prefer rolling-origin conformal intervals before deployment.
