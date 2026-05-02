#!/usr/bin/env python3
from pathlib import Path
import argparse, csv
import numpy as np
import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables-dir", default="results/tables")
    ap.add_argument("--figs-dir", default="results/figures")
    ap.add_argument("--before-cfile", default="/media/patryk/X31/jamguard_processed_test110/test_110_synth_jam_180s/ch0.cfile")
    ap.add_argument("--after-cfile", default="/media/patryk/X31/jamguard_processed_test110/test_110_lcmv_180s/lcmv_ch0ref_null.cfile")
    ap.add_argument("--sample-rate", type=float, default=2_400_000)
    ap.add_argument("--spectrum-n", type=int, default=2**22)
    args = ap.parse_args()

    tables, figs = Path(args.tables_dir), Path(args.figs_dir)
    tables.mkdir(parents=True, exist_ok=True); figs.mkdir(parents=True, exist_ok=True)
    rows = [
        {"segment_s":10,"samples":24_000_000,"jammer_suppression_db":90.33,"gnss_tracking_events":4,"unique_prns_tracked":4,"nav_messages":0,"position_fix":"No"},
        {"segment_s":60,"samples":144_000_000,"jammer_suppression_db":92.00,"gnss_tracking_events":10,"unique_prns_tracked":7,"nav_messages":21,"position_fix":"No"},
        {"segment_s":180,"samples":432_000_000,"jammer_suppression_db":97.18,"gnss_tracking_events":11,"unique_prns_tracked":8,"nav_messages":119,"position_fix":"Yes"},
    ]
    csv_path = tables / "test_110_packaged_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    md_path=tables/"test_110_packaged_results.md"
    md_path.write_text("Controlled synthetic spatial jammer tests on real captures; do not claim real-world immunity or CRPA parity.\n", encoding="utf-8")

    seg=[str(r['segment_s']) for r in rows]
    plt.figure(); plt.bar(seg,[r['jammer_suppression_db'] for r in rows]); plt.tight_layout(); plt.savefig(figs/"test_110_jammer_suppression_vs_duration.png",dpi=200); plt.close()

    before_path, after_path = Path(args.before_cfile), Path(args.after_cfile)
    if before_path.exists() and after_path.exists():
        def spectrum_db(path, n, fs):
            x=np.fromfile(path,dtype=np.complex64,count=n); win=np.hanning(len(x)); X=np.fft.fftshift(np.fft.fft(x*win)); f=np.fft.fftshift(np.fft.fftfreq(len(x),d=1/fs)); p=20*np.log10(np.abs(X)/np.sqrt(np.sum(win**2))+1e-12); return f,p
        fb,pb=spectrum_db(before_path,args.spectrum_n,args.sample_rate); fa,pa=spectrum_db(after_path,args.spectrum_n,args.sample_rate)
        m1=np.abs(fb)<=10_000; m2=np.abs(fa)<=10_000
        plt.figure(); plt.plot(fb[m1]/1000,pb[m1],label='Before'); plt.plot(fa[m2]/1000,pa[m2],label='After'); plt.legend(); plt.tight_layout(); plt.savefig(figs/"test_110_180s_before_after_spectrum.png",dpi=200); plt.close()

    print(csv_path); print(md_path)

if __name__ == '__main__':
    main()
