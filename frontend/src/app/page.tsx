import { EngineStatus } from "@/components/engine-status";
import { NAV } from "@/lib/nav";

export default function Home() {
  const phases = [...NAV].sort((a, b) => a.phase - b.phase);
  return (
    <section className="flex flex-col gap-8">
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl font-semibold tracking-tight">Tax Copilot</h1>
        <p className="max-w-prose text-sm text-muted-foreground">
          Phase 0 scaffold. Net worth, account cards and this year&apos;s income vs spend land here in Phase 8; until
          then this page shows the engine status and what each section will do.
        </p>
      </div>
      <div className="rounded-lg border bg-card p-6">
        <EngineStatus detailed />
      </div>
      <ol className="grid gap-3 sm:grid-cols-2">
        {phases.map(({ href, label, phase, blurb, icon: Icon }) => (
          <li key={href} className="flex gap-3 rounded-lg border bg-card p-4">
            <Icon className="mt-0.5 size-4 shrink-0 text-muted-foreground" />
            <div className="flex flex-col gap-1">
              <span className="text-sm font-medium">
                {label} <span className="text-xs font-normal text-muted-foreground">· Phase {phase}</span>
              </span>
              <span className="text-sm text-muted-foreground">{blurb}</span>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
