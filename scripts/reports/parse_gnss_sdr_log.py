#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, re, statistics

ap = argparse.ArgumentParser()
ap.add_argument("--case-id", required=True)
ap.add_argument("--jammer-kind", required=True)
ap.add_argument("--amplitude", required=True)
ap.add_argument("--branch", required=True)
ap.add_argument("--log", required=True)
ap.add_argument("--out-csv", required=True)
args = ap.parse_args()

text = Path(args.log).read_text(errors="ignore")

tracking_prns = re.findall(r"Tracking of GPS L1/C/A|Tracking of GPS L1 C/A", text)
prns = re.findall(r"Tracking of GPS L1 C/A signal started.*?PRN\s+([0-9]+)", text)
nav = re.findall(r"New GPS NAV message received.*?PRN\s+([0-9]+).*?CN0=([0-9]+(?:\.[0-9]+)?)", text)

cn0 = [float(x[1]) for x in nav]
position_fix = "Yes" if ("First position fix" in text or re.search(r"Position at .* using [0-9]+ observations", text)) else "No"

row = {
    "case_id": args.case_id,
    "jammer_kind": args.jammer_kind,
    "amplitude": args.amplitude,
    "branch": args.branch,
    "tracking_events": len(prns),
    "unique_prns": len(set(prns)),
    "tracked_prns": ",".join(sorted(set(prns))),
    "nav_messages": len(nav),
    "nav_prns": ",".join(sorted(set(x[0] for x in nav))),
    "cn0_count": len(cn0),
    "cn0_min": f"{min(cn0):.2f}" if cn0 else "",
    "cn0_median": f"{statistics.median(cn0):.2f}" if cn0 else "",
    "cn0_max": f"{max(cn0):.2f}" if cn0 else "",
    "loss_of_lock_events": text.count("Loss of lock"),
    "position_fix": position_fix,
    "position_lines": len(re.findall(r"Position at .* using [0-9]+ observations", text)),
}

out = Path(args.out_csv)
out.parent.mkdir(parents=True, exist_ok=True)
write_header = not out.exists()

with out.open("a", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(row.keys()))
    if write_header:
        w.writeheader()
    w.writerow(row)

print(row)
