# Frontend (`packages/web`)

All fetching goes through `services/emailApi.ts` against the relative base `/api`; Vite proxies `/api`
and `/auth` to `http://localhost:8000` (`vite.config.ts`). Production has no equivalent proxy configured.
Data loading and upload validation live in `hooks/useEmailUpload.ts` (10 MB cap, `.eml` extension check)
— keep fetch logic in hooks/services, never in components. `useAuth.ts` is an unwired placeholder polling
`/api/auth/me`, an endpoint that does not exist.
