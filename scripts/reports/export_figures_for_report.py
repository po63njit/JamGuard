#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input', default='')
    ap.add_argument('--output', default='')
    args=ap.parse_args()
    print(f"[JamGuard] running {Path(__file__).name}")
    print(f"input={args.input} output={args.output}")
    if args.output:
        out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
        payload={"script":Path(__file__).name,"input":args.input}
        if out.suffix.lower()=='.json':
            out.write_text(json.dumps(payload, indent=2))
        elif out.suffix.lower()=='.csv':
            out.write_text('key,value\nscript,'+Path(__file__).name+'\n')
        else:
            out.write_text(str(payload))

if __name__=='__main__':
    main()
