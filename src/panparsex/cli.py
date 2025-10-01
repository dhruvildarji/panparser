from __future__ import annotations
import argparse, sys, json, pathlib, glob, os
from .core import parse
from .ai_processor import AIProcessor

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
    
    # AI processing options
    p.add_argument("--ai-process", action="store_true", help="Process with AI after parsing")
    p.add_argument("--ai-task", default="analyze and restructure", help="AI task description")
    p.add_argument("--ai-format", default="structured_json", choices=["structured_json", "markdown", "summary"], help="AI output format")
    p.add_argument("--ai-output", help="Output file for AI-processed result")
    p.add_argument("--openai-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    p.add_argument("--ai-model", default="gpt-4o-mini", help="OpenAI model to use")
    p.add_argument("--ai-tokens", type=int, default=4000, help="Max tokens for AI response")
    p.add_argument("--ai-temperature", type=float, default=0.3, help="AI temperature (0.0-1.0)")

    args = ap.parse_args(argv)

    target = args.target
    pth = pathlib.Path(target)
    docs = []
    parsed_docs = []
    
    if pth.exists() and pth.is_dir():
        for fn in glob.glob(str(pth / args.glob), recursive=True):
            fp = pathlib.Path(fn)
            if fp.is_file():
                d = parse(str(fp), recursive=args.recursive)
                parsed_docs.append(d)
                docs.append(d.model_dump())
    else:
        d = parse(target, recursive=args.recursive, max_links=args.max_links, max_depth=args.max_depth, same_origin=args.same_origin)
        parsed_docs.append(d)
        docs.append(d.model_dump())

    # AI processing
    if args.ai_process:
        try:
            # Use the first document for AI processing (or combine if multiple)
            main_doc = parsed_docs[0] if parsed_docs else None
            if not main_doc:
                print("No documents to process with AI", file=sys.stderr)
                sys.exit(1)
            
            # Determine output file
            output_file = args.ai_output
            if not output_file:
                if args.ai_format == "structured_json":
                    output_file = "ai_processed_result.json"
                elif args.ai_format == "markdown":
                    output_file = "ai_processed_result.md"
                else:
                    output_file = "ai_processed_result.txt"
            
            # Initialize AI processor
            processor = AIProcessor(
                api_key=args.openai_key or os.getenv("OPENAI_API_KEY"),
                model=args.ai_model
            )
            
            # Process with AI
            print(f"Processing with AI (model: {args.ai_model})...", file=sys.stderr)
            result = processor.process_and_save(
                main_doc,
                output_file,
                task=args.ai_task,
                output_format=args.ai_format,
                max_tokens=args.ai_tokens,
                temperature=args.ai_temperature
            )
            
            print(f"AI processing complete. Result saved to: {output_file}", file=sys.stderr)
            
            # Also print the result to stdout if pretty printing is requested
            if args.pretty:
                print("\n=== AI Processed Result ===")
                if args.ai_format == "structured_json" and "raw_response" not in result:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    content = result.get("content", result.get("raw_response", str(result)))
                    print(content)
                print("\n=== Original Parsed Content ===")
                print(json.dumps(docs if len(docs)>1 else docs[0], indent=2, ensure_ascii=False))
            else:
                # Just print original content
                print(json.dumps(docs if len(docs)>1 else docs[0], ensure_ascii=False))
                
        except Exception as e:
            print(f"AI processing failed: {e}", file=sys.stderr)
            print("Falling back to original parsing result...", file=sys.stderr)
            if args.pretty:
                print(json.dumps(docs if len(docs)>1 else docs[0], indent=2, ensure_ascii=False))
            else:
                print(json.dumps(docs if len(docs)>1 else docs[0], ensure_ascii=False))
    else:
        # No AI processing, just print the parsed result
        if args.pretty:
            print(json.dumps(docs if len(docs)>1 else docs[0], indent=2, ensure_ascii=False))
        else:
            print(json.dumps(docs if len(docs)>1 else docs[0], ensure_ascii=False))

if __name__ == "__main__":
    main()
