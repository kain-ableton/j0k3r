#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

def load_products_registry():
    from lib.smartmodules.matchstrings.MatchStrings import get_products_match
    return get_products_match()

PAIR_RX = re.compile(r'(?P<key>[A-Za-z0-9_-]+)\s*[:=]\s*(?P<val>[^,;]+)')
SVC_RX  = re.compile(r'([A-Za-z0-9_]+)\.conf$', re.I)

def parse_context_pairs(text: str):
    # Returns list of (bucket, product_string)
    out = []
    for m in PAIR_RX.finditer(text):
        key = m.group("key").strip()
        raw = m.group("val").strip().strip('"\'')
        # split multiple products by comma or pipe
        parts = re.split(r'\s*[|,]\s*', raw) if raw else []
        if not parts:
            out.append((key, raw))
        else:
            for p in parts:
                if p:
                    out.append((key, p))
    return out

def iter_conf_files(root: Path):
    # Scan the repository for .conf files (service confs like http.conf, ssh.conf, etc.)
    for p in root.rglob("*.conf"):
        # skip OS/system confs if any slipped in
        if ".venv" in p.parts or "site-packages" in p.parts or ".git" in p.parts:
            continue
        yield p

def bucket_alias_map(service: str, reg: dict):
    # Allow alias buckets (e.g., 'web-framework' -> 'framework', 'web-appserver' -> 'appserver')
    svc = reg.get(service, {})
    alias = {}
    # Prefer explicit aliasing if present in registry (e.g., http['web-framework'] is the same list)
    for k, v in svc.items():
        if isinstance(v, list):
            alias[k] = k
    # Common aliases (idempotent)
    if service == "http":
        alias.setdefault("web-framework", "framework")
        alias.setdefault("web-appserver", "appserver")
    return alias

def matcher_for_bucket(patterns):
    # Build case-insensitive regex matchers from registry patterns
    regexes = []
    for pat in patterns:
        try:
            regexes.append(re.compile(pat, re.I))
        except re.error:
            # Fallback: direct case-insensitive equality
            regexes.append(re.compile(rf'^{re.escape(pat)}$', re.I))
    return regexes

def product_in_bucket(product: str, patterns) -> bool:
    rx = matcher_for_bucket(patterns)
    return any(r.search(product) for r in rx)

def main():
    ap = argparse.ArgumentParser(description="Validate context requirements products against product registries")
    ap.add_argument("--root", default=".", help="project root")
    ap.add_argument("--json", action="store_true", help="emit JSON report")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    reg  = load_products_registry()

    errors = []
    scanned = 0

    for conf in iter_conf_files(root):
        m = SVC_RX.search(conf.name)
        if not m:
            continue
        service = m.group(1).lower()
        svc_reg = reg.get(service, {})
        aliases = bucket_alias_map(service, reg)

        text = conf.read_text(encoding="utf-8", errors="ignore")
        # rough section extraction: look for lines with keys like "context_1 = bucket: product"
        context_lines = [ln for ln in text.splitlines() if ln.strip().lower().startswith("context_")]
        if not context_lines:
            continue
        scanned += 1

        for ln in context_lines:
            pairs = parse_context_pairs(ln)
            for bucket, product in pairs:
                if not bucket or not product:
                    continue
                canon = aliases.get(bucket, bucket)
                patterns = svc_reg.get(canon)
                if patterns is None:
                    errors.append({
                        "file": str(conf.relative_to(root)),
                        "service": service,
                        "bucket": bucket,
                        "product": product,
                        "reason": f"unknown bucket; registry has: {sorted(svc_reg.keys())}"
                    })
                    continue
                if not product_in_bucket(product, patterns):
                    errors.append({
                        "file": str(conf.relative_to(root)),
                        "service": service,
                        "bucket": bucket,
                        "product": product,
                        "reason": "no matching pattern in registry"
                    })

    report = {
        "scanned_confs": scanned,
        "errors": errors,
        "error_count": len(errors),
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if not errors:
            print(f"OK: {scanned} service conf(s) validated")
        else:
            print(f"Invalid context products: {len(errors)}")
            for e in errors:
                print(f"- {e['file']} [{e['service']}] {e['bucket']}: \"{e['product']}\" -> {e['reason']}")
    # non-zero exit on errors
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
