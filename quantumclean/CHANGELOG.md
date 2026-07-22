# Changelog

All notable changes to QuantumClean are documented here.
This project follows [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-07-24
### Added
- Three real-world case studies (customer validation, transaction anomalies, pipeline governance).
- Automated release pipeline (GitHub Actions) that tests, builds, and checks the package on version tags.
- Full API documentation and quick-start tutorial in the README.
- CHANGELOG and stable public API commitment.
### Notes
- First stable release. The public API is now considered stable under semantic versioning:
  breaking changes will require a 2.0.0 release.

## [0.3.0] - 2026-07-06
### Added
- `LineageTracker` for data provenance (sources + timestamped operations).
- `QualitySLA` with breach detection and SLA reports.
- `DuckDBBackend` (SQL execution) and `SparkBackend` (distributed) behind `get_backend()`.

## [0.2.0] - 2026-06-17
### Added
- Anomaly detection: `StatisticalOutlierDetector` (z-score/IQR) and `IsolationForestDetector` (ML).
- `QualityScorer` with four metrics (completeness, uniqueness, validity, consistency).
- Backend abstraction layer with `PandasBackend` and `get_backend()` factory.

## [0.1.0] - 2026-06-03
### Added
- Core validation engine: `BaseValidator` + six validators (NotNull, Email, Range, Regex, Unique, Categorical).
- `Schema` runner and `ValidationResult` / `SchemaResult` objects.
