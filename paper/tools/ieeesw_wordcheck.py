#!/usr/bin/env python3
"""
ieeesw_wordcheck.py

IEEE Software word-count checker for LaTeX (.tex) files.

Rules implemented:
- Total <= 4200 words, including:
  - +250 words per figure
  - +250 words per table
  - +250 words per code block (verbatim/listings/minted/etc.)
- Inline equations counted as regular text
- Abstract <= 150 words
- Max 15 references (not included in word count)
- Author bios not included in the word count (reported separately)

Usage:
  python ieeesw_wordcheck.py main.tex
  python ieeesw_wordcheck.py main.tex --expand-inputs
  python ieeesw_wordcheck.py main.tex --json

Exit code:
  0 if all hard limits pass, else 2
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# -------------------------
# Document body extraction
# -------------------------

DOCUMENT_RE = re.compile(
    r"\\begin\{document\}(?P<body>.*?)\\end\{document\}",
    re.DOTALL,
)

def extract_document_body(tex: str) -> str:
    """
    Return only the content between \\begin{document} and \\end{document}.
    If not found, return the original text (fail-soft behavior).
    """
    m = DOCUMENT_RE.search(tex)
    if not m:
        return tex
    return m.group("body")


# -------------------------
# Tokenization / word count
# -------------------------

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


# -------------------------
# LaTeX preprocessing
# -------------------------

def strip_comments(tex: str) -> str:
    """Remove LaTeX comments, respecting escaped percent \\%."""
    lines = []
    for line in tex.splitlines():
        out = []
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            out.append(ch)
            i += 1
        lines.append("".join(out))
    return "\n".join(lines)


def read_text_file(path: Path) -> str:
    # Try UTF-8 first, fallback to latin-1
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


INPUT_CMD_RE = re.compile(r"\\(input|include)\{([^}]+)\}")


def expand_inputs(tex: str, base_dir: Path, seen: Set[Path]) -> str:
    """Recursively expand \\input{...} and \\include{...} using base_dir resolution."""
    def repl(match: re.Match) -> str:
        fname = match.group(2).strip()
        p = (base_dir / fname)
        candidates = [p] if p.suffix.lower() == ".tex" else [p, p.with_suffix(".tex")]

        target = None
        for cp in candidates:
            if cp.exists() and cp.is_file():
                target = cp.resolve()
                break
        if not target:
            return match.group(0)

        if target in seen:
            return ""
        seen.add(target)

        content = strip_comments(read_text_file(target))
        content = expand_inputs(content, target.parent, seen)
        return "\n" + content + "\n"

    prev = None
    cur = tex
    for _ in range(50):
        prev = cur
        cur = INPUT_CMD_RE.sub(repl, cur)
        if cur == prev:
            break
    return cur


# -------------------------
# Environment extraction
# -------------------------

def extract_env_blocks(tex: str, env_names: List[str]) -> Tuple[str, Dict[str, List[str]]]:
    """
    Extract \\begin{env}...\\end{env} blocks (non-nested heuristic),
    returning (tex_without_blocks, blocks_by_env).
    Supports starred forms: env*
    """
    blocks: Dict[str, List[str]] = {e: [] for e in env_names}
    env_alt = "|".join(re.escape(e) for e in env_names)
    pattern = re.compile(
        rf"\\begin\{{(?P<env>{env_alt})\*?\}}(?P<body>.*?)\\end\{{(?P=env)\*?\}}",
        re.DOTALL,
    )

    def repl(m: re.Match) -> str:
        env = m.group("env")
        blocks[env].append(m.group(0))
        return "\n"

    out = pattern.sub(repl, tex)
    return out, blocks


# -------------------------
# LaTeX -> plain-ish text
# -------------------------

HREF_RE = re.compile(r"\\href\{[^}]*\}\{([^}]*)\}")
URL_RE = re.compile(r"\\url\{([^}]*)\}")
CITE_RE = re.compile(r"\\cite[t|p]?\*?(?:\[[^\]]*\])?\{[^}]*\}")  # \cite, \citet, \citep, etc.
LABEL_RE = re.compile(r"\\label\s*(?:\[[^\]]*\])?\s*\{[^}]*\}")

SINGLE_ARG_CMDS_RE = re.compile(
    r"\\(?:sptitle|title|author|affil)\*?"
    r"(?:\[[^\]]*\])?\s*\{[^{}]*\}",
    re.DOTALL,
)

MARKBOTH_RE = re.compile(
    r"\\markboth\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}\s*\{[^{}]*\}",
    re.DOTALL,
)

def latex_to_text(tex: str) -> str:
    """
    Lightweight LaTeX-to-text cleanup for word counting.
    Keeps inline math content (doesn't remove $...$), per your rules.
    """
    t = tex

    # Keep link text; keep URL literal (counts as tokens)
    t = HREF_RE.sub(r"\1", t)
    t = URL_RE.sub(r"\1", t)

    # Drop citation commands (the cite keys themselves don't inflate count)
    t = CITE_RE.sub(" ", t)
    t = LABEL_RE.sub(" ", t)

    # --- IMPORTANT: remove multi-argument commands FIRST ---

    # Drop \markboth{left}{right} completely
    t = MARKBOTH_RE.sub(" ", t)

    # Drop title/author-style commands completely
    t = SINGLE_ARG_CMDS_RE.sub(" ", t)

    # --- Then unwrap normal formatting commands (iteratively) ---

    # Remove common formatting commands while keeping their argument content
    # Iterate to handle shallow nesting (e.g., \textbf{\emph{word}})
    for _ in range(5):
        t_new = re.sub(
            r"\\[A-Za-z@]+(?:\*?)\s*(?:\[[^\]]*\])?\s*\{([^{}]*)\}",
            r"\1",
            t,
        )
        if t_new == t:
            break
        t = t_new

    # Remove remaining commands like \command or \command*
    t = re.sub(r"\\[A-Za-z@]+(?:\*?)\b", " ", t)

    # Remove braces
    t = t.replace("{", " ").replace("}", " ")

    # Normalize whitespace
    t = re.sub(r"\s+", " ", t).strip()
    return t


# -------------------------
# References counting
# -------------------------

BIBLIOGRAPHY_CMD_RE = re.compile(r"\\bibliography\{([^}]+)\}")


def count_references(tex: str, tex_path: Path) -> Tuple[int, str]:
    """
    Best-effort reference count:
    1) If the .tex has thebibliography, count \\bibitem entries there
    2) Else if a sibling .bbl exists, count \\bibitem there
    3) Else if \\bibliography{...} points to .bib, count entries in .bib
    Returns (count, method_string)
    """
    if "\\begin{thebibliography}" in tex:
        return len(re.findall(r"\\bibitem\b", tex)), "thebibliography in .tex"

    bbl = tex_path.with_suffix(".bbl")
    if bbl.exists():
        bbl_text = strip_comments(read_text_file(bbl))
        return len(re.findall(r"\\bibitem\b", bbl_text)), f".bbl file ({bbl.name})"

    m = BIBLIOGRAPHY_CMD_RE.search(tex)
    if m:
        bibs = [p.strip() for p in m.group(1).split(",") if p.strip()]
        for bibstem in bibs:
            candidate = (tex_path.parent / bibstem)
            if candidate.suffix.lower() != ".bib":
                candidate = candidate.with_suffix(".bib")
            if candidate.exists():
                bib_text = strip_comments(read_text_file(candidate))
                entries = len(re.findall(r"^\s*@\w+\s*\{", bib_text, flags=re.MULTILINE))
                return entries, f".bib file ({candidate.name})"
        return 0, "bibliography command found, but .bib not resolved"

    return 0, "no bibliography source found"


# -------------------------
# Main analysis
# -------------------------

@dataclass
class Report:
    files: List[str]
    expanded_inputs: bool

    abstract_words: int
    main_text_words: int

    figure_count: int
    table_count: int
    code_block_count: int

    added_words_fig_tab: int
    added_words_code: int
    total_counted_words: int

    references_count: int
    references_method: str

    biography_words: int

    limits: Dict[str, object]


CODE_ENVS = ["verbatim", "Verbatim", "lstlisting", "minted", "code"]
FIG_ENVS = ["figure"]
TAB_ENVS = ["table"]


def analyze_tex_file(path: Path, expand: bool) -> Report:
    
    # Strip comments
    tex = strip_comments(read_text_file(path))

    # Expand inputs/includes if requested
    if expand:
        tex = expand_inputs(tex, path.parent, seen={path.resolve()})

    # Extract document body
    tex_all = extract_document_body(tex)

    # Extract abstract (counted)
    tex_no_abstract, abstract_blocks = extract_env_blocks(tex_all, ["abstract"])
    abstract_words = 0
    if abstract_blocks["abstract"]:
        abstract_plain = latex_to_text("\n".join(abstract_blocks["abstract"]))
        abstract_words = count_words(abstract_plain)

    # References count (not counted)
    references_count, references_method = count_references(tex_all, path)

    # Remove references content from counted text
    tex_wo_bib, _ = extract_env_blocks(tex_no_abstract, ["thebibliography"])
    tex_wo_bib = BIBLIOGRAPHY_CMD_RE.sub(" ", tex_wo_bib)
    tex_wo_bib = re.sub(r"\\bibliographystyle\{[^}]*\}", " ", tex_wo_bib)

    # Remove bios from counted text, but count them separately
    tex_wo_bio, bio_blocks = extract_env_blocks(tex_wo_bib, ["IEEEbiography"])
    bio_plain = latex_to_text("\n".join(bio_blocks["IEEEbiography"]))
    biography_words = count_words(bio_plain)

    # Figures
    tex_wo_fig, fig_blocks = extract_env_blocks(tex_wo_bio, FIG_ENVS)
    figure_count = len(fig_blocks["figure"])

    # Tables
    tex_wo_tab, tab_blocks = extract_env_blocks(tex_wo_fig, TAB_ENVS)
    table_count = len(tab_blocks["table"])

    # Code blocks
    tex_wo_code = tex_wo_tab
    code_block_count = 0
    for env in CODE_ENVS:
        tex_wo_code, blocks = extract_env_blocks(tex_wo_code, [env])
        code_block_count += len(blocks[env])

    # Main text word count
    main_plain = latex_to_text(tex_wo_code)
    #print(main_plain)
    main_text_words = count_words(main_plain)

    # Add rule-based increments
    added_words_fig_tab = 250 * (figure_count + table_count)
    added_words_code = 250 * code_block_count
    total_counted_words = abstract_words + main_text_words + added_words_fig_tab + added_words_code

    limits = {
        "abstract_max_150": (abstract_words <= 150),
        "total_max_4200": (total_counted_words <= 4200),
        "references_max_15": (references_count <= 15) if references_count > 0 else None,  # None if unknown
    }

    return Report(
        files=[str(path)],
        expanded_inputs=expand,

        abstract_words=abstract_words,
        main_text_words=main_text_words,

        figure_count=figure_count,
        table_count=table_count,
        code_block_count=code_block_count,

        added_words_fig_tab=added_words_fig_tab,
        added_words_code=added_words_code,
        total_counted_words=total_counted_words,

        references_count=references_count,
        references_method=references_method,

        biography_words=biography_words,

        limits=limits,
    )


def format_report_human(r: Report) -> str:
    lines = []
    lines.append("IEEE Software Word Count Check")
    lines.append("=" * 32)
    lines.append(f"Files: {', '.join(r.files)}")
    lines.append(f"Expanded \\\\input/\\\\include: {r.expanded_inputs}")
    lines.append("")

    lines.append("Word counts")
    lines.append("-" * 32)
    lines.append(f"Abstract words:              {r.abstract_words}   (limit 150)")
    lines.append(f"Main text words:             {r.main_text_words}")
    lines.append(f"Figures:                     {r.figure_count}   (+{r.added_words_fig_tab} words)")
    lines.append(f"Tables:                      {r.table_count}   (included in +250 rule above)")
    lines.append(f"Code blocks:                 {r.code_block_count}   (+{r.added_words_code} words)")
    lines.append(f"TOTAL COUNTED WORDS:         {r.total_counted_words}   (limit 4200)")
    lines.append("")

    lines.append("References & bios (not included in word count)")
    lines.append("-" * 32)
    lines.append(f"References count:            {r.references_count}   (limit 15)  [{r.references_method}]")
    lines.append(f"Biography words (excluded):  {r.biography_words}")
    lines.append("")

    lines.append("Hard-limit checks")
    lines.append("-" * 32)
    lines.append(f"Abstract <= 150:     {r.limits['abstract_max_150']}")
    lines.append(f"Total <= 4200:       {r.limits['total_max_4200']}")
    if r.limits["references_max_15"] is None:
        lines.append("References <= 15:    unknown (couldn't resolve references source)")
    else:
        lines.append(f"References <= 15:    {r.limits['references_max_15']}")

    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="IEEE Software LaTeX word-count checker")
    parser.add_argument("tex_file", help="Main .tex file (entry point).")
    parser.add_argument("--expand-inputs", action="store_true",
                        help="Recursively expand \\\\input{...} and \\\\include{...}.")
    parser.add_argument("--json", action="store_true", help="Output JSON report.")
    args = parser.parse_args(argv)

    path = Path(args.tex_file).expanduser().resolve()
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    report = analyze_tex_file(path, expand=args.expand_inputs)

    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print(format_report_human(report))

    # Hard pass/fail (treat unknown refs as non-failing but warn in report)
    hard_ok = report.limits["abstract_max_150"] and report.limits["total_max_4200"]
    if report.limits["references_max_15"] is False:
        hard_ok = False

    return 0 if hard_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
