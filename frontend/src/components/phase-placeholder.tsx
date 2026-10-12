import { NAV } from "@/lib/nav";

export function PhasePlaceholder({ href }: { href: string }) {
  const item = NAV.find((n) => n.href === href);
  if (!item) return null;
  const Icon = item.icon;
  return (
    <section className="flex flex-col gap-6">
      <h1 className="text-2xl font-semibold tracking-tight">{item.label}</h1>
      <div className="flex flex-col items-start gap-3 rounded-lg border border-dashed bg-card p-8">
        <Icon className="size-6 text-muted-foreground" />
        <p className="max-w-prose text-sm text-muted-foreground">{item.blurb}</p>
        <span className="rounded-full bg-accent px-2.5 py-0.5 text-xs font-medium text-accent-foreground">
          Arrives in Phase {item.phase}
        </span>
      </div>
    </section>
  );
}
