import {
  ArrowLeftRight,
  CalendarClock,
  Home,
  Inbox,
  LineChart,
  ListOrdered,
  Receipt,
  Settings,
  Upload,
  type LucideIcon,
} from "lucide-react";

export type NavItem = { href: string; label: string; icon: LucideIcon; phase: number; blurb: string };

export const NAV: NavItem[] = [
  { href: "/", label: "Home", icon: Home, phase: 8, blurb: "Account cards, net worth over time, allocation, and this year's income vs spend." },
  { href: "/upload", label: "Upload", icon: Upload, phase: 1, blurb: "Drop statements and tax documents; see detection, tie-out and a coverage calendar per account." },
  { href: "/timeline", label: "Timeline", icon: ListOrdered, phase: 1, blurb: "Every transaction across accounts in one ledger, with linked events collapsed into one row." },
  { href: "/flow", label: "Money Flow", icon: ArrowLeftRight, phase: 2, blurb: "Where money came from and went, between your own accounts and out of them." },
  { href: "/review", label: "Review", icon: Inbox, phase: 2, blurb: "Proposed links and low-confidence categories, one keystroke to accept, reject or make a rule." },
  { href: "/investments", label: "Investments", icon: LineChart, phase: 5, blurb: "Holdings, FIFO lots, realised and unrealised gains by tax bucket, upcoming LTCG thresholds." },
  { href: "/tax", label: "Tax", icon: Receipt, phase: 4, blurb: "Old vs new regime, the full computation with drill-down to source rows, AIS mismatches, ITR fill sheet." },
  { href: "/plan", label: "Plan", icon: CalendarClock, phase: 7, blurb: "Current-year projection, advance tax, harvesting and regime suggestions with rupee impact." },
  { href: "/settings", label: "Rules & Settings", icon: Settings, phase: 3, blurb: "Your rules, rule-file versions and verification status, LLM toggle, export and wipe." },
];
