# Frontend

Next.js (App Router) + TypeScript + Tailwind. Run from the repo root with `make dev`; this app proxies
`/api/*` to the Python engine on 127.0.0.1:8000 (see `next.config.ts`).

shadcn/ui conventions are configured (`components.json`, `@/lib/utils`); components are added into
`src/components/ui` as they are needed.
