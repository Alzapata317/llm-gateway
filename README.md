# LLM Gateway

An OpenAI-compatible gateway that sits in front of multiple LLM providers,
providing a single API surface with request logging, cost attribution,
routing, and failover.

**Status: early development.** Not usable yet.

## Why

Applications that talk to multiple LLM providers end up with provider-specific
branching scattered through the codebase, no unified view of spend, and no
shared failover behavior. This gateway exposes one OpenAI-compatible endpoint
and handles provider differences behind it.

Because the surface is OpenAI-compatible, existing client code works by
changing `base_url` alone.

## Planned scope

- [ ] OpenAI-compatible `/v1/chat/completions`, streaming and non-streaming
- [ ] Anthropic backend via bidirectional wire-format translation
- [ ] Per-request cost attribution and latency breakdown (TTFT, inter-token)
- [ ] Model aliasing, routing rules, and failover
- [ ] API keys with per-key budgets and rate limits
- [ ] Semantic response cache, evaluated for false-hit rate
- [ ] Self-hosted vLLM backend with cost break-even analysis

## Stack

Python 3.12, FastAPI, httpx, Postgres, SQLAlchemy 2.0 (async), uv.

## Development

```bash
uv sync
uv run uvicorn app.main:app --reload
```

## License

MIT