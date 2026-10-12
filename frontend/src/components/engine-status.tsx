"use client";

import { useEffect, useState } from "react";

import { cn } from "@/lib/utils";

type Health = { status: string; version: string; schema_revision: string | null; parsers: string[]; llm_enabled: boolean };

export function EngineStatus({ detailed = false }: { detailed?: boolean }) {
  const [health, setHealth] = useState<Health | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetch("/api/health")
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then((h: Health) => !cancelled && setHealth(h))
      .catch(() => !cancelled && setFailed(true));
    return () => {
      cancelled = true;
    };
  }, []);

  const ok = health?.status === "ok";
  const label = ok ? "Engine connected" : failed ? "Engine offline" : "Connecting…";

  return (
    <div className="flex flex-col gap-1">
      <span className="inline-flex items-center gap-2 text-xs text-muted-foreground">
        <span className={cn("size-2 rounded-full", ok ? "bg-positive" : failed ? "bg-negative" : "bg-warning")} />
        {label}
      </span>
      {detailed && ok && health && (
        <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1 text-sm">
          <dt className="text-muted-foreground">Engine version</dt>
          <dd>{health.version}</dd>
          <dt className="text-muted-foreground">Schema revision</dt>
          <dd>{health.schema_revision ?? "not migrated"}</dd>
          <dt className="text-muted-foreground">Parsers registered</dt>
          <dd>{health.parsers.length === 0 ? "none yet (Phase 1)" : health.parsers.join(", ")}</dd>
          <dt className="text-muted-foreground">LLM assist</dt>
          <dd>{health.llm_enabled ? "on" : "off"}</dd>
        </dl>
      )}
      {detailed && failed && (
        <p className="text-sm text-muted-foreground">
          Start everything with <code className="rounded bg-muted px-1">make dev</code>.
        </p>
      )}
    </div>
  );
}
