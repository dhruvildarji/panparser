from __future__ import annotations
import argparse, sys, json, pathlib, glob
from .core import parse

def main(argv=None):
    argv = argv or sys.argv[1:]
    ap = argparse.ArgumentParser(prog="panparsex", description="Universal parser for files and websites")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("parse", help="Parse a path, file, or URL")
    p.add_argument("target", help="Path/URL to parse")
    p.add_argument("--recursive", action="store_true", help="Recurse into folders or follow links")
    p.add_argument("--glob", default="**/*", help="Glob when target is a folder")
    p.add_argument("--max-links", type=int, default=50, help="Max links/pages when crawling")
    p.add_argument("--max-depth", type=int, default=1, help="Max depth when crawling")
    p.add_argument("--same-origin", action="store_true", help="Restrict crawl to same origin")
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    args = ap.parse_args(argv)

    target = args.target
    pth = pathlib.Path(target)
    docs = []
    if pth.exists() and pth.is_dir():
        for fn in glob.glob(str(pth / args.glob), recursive=True):
            fp = pathlib.Path(fn)
            if fp.is_file():
                d = parse(str(fp), recursive=args.recursive)
                docs.append(d.model_dump())
    else:
        d = parse(target, recursive=args.recursive, max_links=args.max_links, max_depth=args.max_depth, same_origin=args.same_origin)
        docs.append(d.model_dump())

    if args.pretty:
        print(json.dumps(docs if len(docs)>1 else docs[0], indent=2, ensure_ascii=False))
    else:
        print(json.dumps(docs if len(docs)>1 else docs[0], ensure_ascii=False))

if __name__ == "__main__":
    main()
