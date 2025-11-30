# Security, API, and Performance

## Security Best Practices

* Never commit secrets
* Always validate user input
* Use parameterized queries
* Keep dependencies updated
* Use HTTPS for external services
* Implement proper authentication & authorization

## API Standards

Maintain consistent route naming, parameter naming, and field naming.

## Performance Guidelines

* Profile before optimizing
* Prefer generators for streaming workloads
* Use caching (`lru_cache`) for expensive pure functions
* Use asyncio for I/O-bound tasks
* Use multiprocessing for CPU-bound tasks
