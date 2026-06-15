"""The agent-run company.

Goal: run the business with ~0 payroll. The architecture is a Manager -> Doer hierarchy per
department, plus a Chief of Staff that reports to the (human) founder. Salvaged from the
shelved `vero` project's department model and re-pointed at the marketing-OS business.

ACTIVATION POLICY (read this before turning anything on):
- Do NOT activate a department before it has real work. A Finance manager reconciling $0 of
  revenue is theater. Pre-revenue, only the Delivery loop and the Chief of Staff are active.
- "0 payroll" means no employees. It does NOT mean no humans in any loop. The CUSTOMER's
  approval of a budget change stays human by design — that governance gate is the product's
  trust feature, not headcount to automate away. Same for signing contracts and the founder's
  own judgment calls.
- Flip `active=True` on a role only when that function's volume justifies it, and write the
  trigger in `activate_when`.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgentRole:
    name: str
    department: str
    kind: str            # 'manager' | 'doer'
    cadence: str         # 'webhook' | 'daily' | 'weekly' | 'on_demand'
    active: bool         # is this running now?
    activate_when: str   # the condition that should flip it on
    model: str = "claude-sonnet-4-6"


# The company. Most roles are intentionally dormant until there's work for them.
ORG: list[AgentRole] = [
    # --- DELIVERY: the product loop. This is the business; it's active. ---
    AgentRole("Delivery Manager", "delivery", "manager", "weekly", True,
              "active from day one — owns the recommend->approve->execute->measure loop",
              model="claude-opus-4-8"),
    AgentRole("Recommender", "delivery", "doer", "on_demand", True,
              "active — turns a property's data into three ranked budget options"),
    AgentRole("Attribution/Reporting", "delivery", "doer", "weekly", True,
              "active — computes incremental tours and writes the operator-facing report"),
    # NOTE: execution is NOT an agent. A human buyer approves; core.approvals gates it.

    # --- GROWTH: acquiring properties/customers. Dormant until you sell outside the base. ---
    AgentRole("Growth Manager", "growth", "manager", "weekly", False,
              "activate when selling beyond the initial captive base"),
    AgentRole("Prospector", "growth", "doer", "daily", False,
              "activate when you have a repeatable outbound motion to run"),
    AgentRole("Outreach Writer", "growth", "doer", "daily", False,
              "activate alongside Prospector"),

    # --- CUSTOMER SUCCESS: dormant until there are customers to keep. ---
    AgentRole("CS Manager", "customer_success", "manager", "weekly", False,
              "activate at >1 paying property"),
    AgentRole("Onboarding", "customer_success", "doer", "webhook", False,
              "activate when onboarding volume > founder can handle by hand"),
    AgentRole("Renewal/Expansion", "customer_success", "doer", "daily", False,
              "activate when first contracts approach renewal"),

    # --- FINANCE: dormant until there's revenue to reconcile. ---
    AgentRole("Finance Manager", "finance", "manager", "weekly", False,
              "activate when monthly invoices exist"),
    AgentRole("Billing/Reconciliation", "finance", "doer", "daily", False,
              "activate when billing on tours goes live"),

    # --- SUPPORT: dormant until inbound exists. ---
    AgentRole("Support Manager", "support", "manager", "daily", False,
              "activate when inbound support volume is real"),

    # --- INTELLIGENCE: low priority; competitive + performance synthesis. ---
    AgentRole("Competitive/Perf Monitor", "intelligence", "doer", "weekly", False,
              "activate once the core loop is stable"),

    # --- CHIEF OF STAFF: synthesizes everything for the founder. Useful immediately. ---
    AgentRole("Chief of Staff", "exec", "manager", "weekly", True,
              "active — weekly briefing to the founder; the human stays in command",
              model="claude-opus-4-8"),
]


def active_roles() -> list[AgentRole]:
    return [r for r in ORG if r.active]


def dormant_roles() -> list[AgentRole]:
    return [r for r in ORG if not r.active]


def org_status() -> str:
    """Human-readable headcount-of-agents view: what's running vs. waiting, and why."""
    lines = [f"AGENT-RUN COMPANY — {len(active_roles())} active / {len(dormant_roles())} dormant", ""]
    by_dept: dict[str, list[AgentRole]] = {}
    for r in ORG:
        by_dept.setdefault(r.department, []).append(r)
    for dept, roles in by_dept.items():
        lines.append(f"[{dept}]")
        for r in roles:
            flag = "ON " if r.active else "off"
            lines.append(f"  {flag}  {r.name:24} ({r.kind}, {r.cadence}) — {r.activate_when}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(org_status())
