"""
Daily scheduler for the FullyVital SEO project (run by launchd at 9:00; safe to run any time).

Schedule: data/processed/schedule.json. Each task has an id, a due date, an optional repeat (days), and either:
  - "run": a command to execute (read-only checks and reports, or spend already approved by the user), or
  - "remind": a message shown as a macOS notification (decisions that need the user or a Claude session).
Due tasks run once, the result is logged to data/processed/scheduler_log.jsonl and reports/scheduler-status.md,
then the task is marked done or moved to its next date.

Usage:
    python fv_scheduler.py            # run what's due today
    python fv_scheduler.py --list     # show the schedule
"""
import json
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHED = ROOT / "data/processed/schedule.json"
LOG = ROOT / "data/processed/scheduler_log.jsonl"
STATUS = ROOT / "reports/scheduler-status.md"
PY = str(ROOT / ".venv/bin/python")


def notify(title, msg):
    subprocess.run(["osascript", "-e", f'display notification {json.dumps(msg)} with title {json.dumps(title)} sound name "Glass"'], check=False)


def main():
    tasks = json.loads(SCHED.read_text())
    if "--list" in sys.argv:
        for t in sorted(tasks, key=lambda t: t["due"]):
            print(f'{t["due"]}  {"done" if t.get("done") else "    "}  {t["id"]}: {t.get("run") or t.get("remind")}')
        return
    today = date.today()
    for t in tasks:
        if t.get("done") or date.fromisoformat(t["due"]) > today:
            continue
        rec = {"ts": datetime.now().isoformat(timespec="seconds"), "id": t["id"]}
        if t.get("run"):
            r = subprocess.run([PY if a == "python" else a for a in t["run"]], cwd=ROOT, capture_output=True, text=True, timeout=3600)
            rec.update(returncode=r.returncode, out=r.stdout[-800:], err=r.stderr[-400:])
            notify("FullyVital SEO", f'{t["id"]}: {"done" if r.returncode == 0 else "FAILED, check reports/scheduler-status.md"}. {t.get("note", "")}')
        else:
            notify("FullyVital SEO reminder", t["remind"])
            rec["reminded"] = t["remind"]
        with LOG.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        t["last_run"] = rec["ts"]
        if t.get("repeat_days"):
            t["due"] = str(max(today, date.fromisoformat(t["due"])) + timedelta(days=t["repeat_days"]))
        else:
            t["done"] = True
    SCHED.write_text(json.dumps(tasks, indent=1))
    lines = ["# Scheduler status", "", f"Last checked {datetime.now():%Y-%m-%d %H:%M}. Runs daily at 9:00 (launch agent `com.fullyvital.scheduler`).", "",
             "| Due | Task | Type | Last run |", "|---|---|---|---|"]
    for t in sorted(tasks, key=lambda t: (bool(t.get("done")), t["due"])):
        lines.append(f'| {"done" if t.get("done") else t["due"]} | {t["id"]} | {"runs automatically" if t.get("run") else "reminder for you"} | {t.get("last_run", "")} |')
    STATUS.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
