"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

import { EngineStatus } from "@/components/engine-status";
import { ThemeToggle } from "@/components/theme-toggle";
import { NAV } from "@/lib/nav";
import { cn } from "@/lib/utils";

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const isActive = (href: string) => (href === "/" ? pathname === "/" : pathname.startsWith(href));

  return (
    <div className="flex min-h-dvh">
      <aside className="sticky top-0 hidden h-dvh w-60 shrink-0 flex-col border-r px-3 py-5 md:flex">
        <div className="px-3 pb-6 text-sm font-semibold tracking-tight">Tax Copilot</div>
        <nav className="flex flex-col gap-0.5">
          {NAV.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground",
                isActive(href) && "bg-accent text-accent-foreground hover:bg-accent hover:text-accent-foreground",
              )}
            >
              <Icon className="size-4" />
              {label}
            </Link>
          ))}
        </nav>
        <div className="mt-auto flex items-center justify-between px-3">
          <EngineStatus />
          <ThemeToggle />
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex items-center justify-between border-b px-4 py-3 md:hidden">
          <span className="text-sm font-semibold">Tax Copilot</span>
          <div className="flex items-center gap-3">
            <EngineStatus />
            <ThemeToggle />
          </div>
        </header>

        <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-6 pb-24 md:px-8 md:py-10 md:pb-10">{children}</main>

        <footer className="border-t px-4 py-3 pb-20 text-center text-xs text-muted-foreground md:pb-3">
          Decision support, not professional tax advice. Your data stays on this machine; you file on the
          income-tax portal yourself.
        </footer>
      </div>

      <nav className="fixed inset-x-0 bottom-0 flex overflow-x-auto border-t bg-background md:hidden">
        {NAV.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={cn(
              "flex min-w-16 flex-1 flex-col items-center gap-1 px-2 py-2 text-[10px] text-muted-foreground",
              isActive(href) && "text-primary",
            )}
          >
            <Icon className="size-5" />
            <span className="truncate">{label}</span>
          </Link>
        ))}
      </nav>
    </div>
  );
}
