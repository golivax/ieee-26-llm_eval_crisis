# Project Overview

This project is a work-in-progress article for IEEE Software magazine. IEEE Software is a practitioner-focused magazine, not a pure research journal. Its goal is to bridge the gap between software research and real-world practice. Think: "How can this help working software developers, architects, and managers do their jobs better?" 

## Audience 

The audience is composed of practicing software engineers, architects, managers, and educators. This is broad audience, so deep specialization cannot be assumed. The audience wishes actionable insights.

## Content focus

The article should emphasize practical experience, such as:
- How software is built in real organizations (industry, labs, universities)
- What worked, what didn’t, and why
- Lessons learned from successes and failures
- Tools, architectures, processes, or methods used in practice
- Evidence from real projects (lightweight empirical data is welcome)

The article **must contain three actionable insights**.

## IEEE Software Requirements

### Word Count Structure
- **Total limit**: 4200 words
- **Abstract limit**: 150 words
- **References limit**: 15 (not counted in word total)
- **Biographies**: Not counted in word total
- **Figures/Tables/Code blocks**: Each counts as +250 words

### Writing Style
- **Strictly avoid dashes and semicolons for sentence separation**: no `--` (en-dashes), no `—` or `---` (em-dashes), and no semicolons (`;`). Use parentheses, colons, or sentence breaks instead.
- Use American English with serial comma ("a, b, and c")
- Define all acronyms at first mention in abstract and main text
- Spell out numerals up to ten without units; use digits with units
- Figure callouts: Always use LaTeX cross-references (e.g., `Figure~\ref{fig:label}`), never hardcode numbers like "Figure 1"
- Lists: Use `\ieeeguilsinglright` bullet style with periods ending each item

### Document Structure
- Abstract: Single paragraph summarizing work, no citations
- Introduction: Background, purpose, relevant citations
- Body sections: Present results and findings
- Conclusion: Include future directions; avoid referencing multiple figures/tables
- Acknowledgments: Appears after conclusion, before references (American spelling: two e's)
- Biographies: One paragraph each; first author includes contact email
- Section titles: Top-level section titles must be UPPERCASE (e.g., `\section{CONCLUSION}`, not `\section{Conclusion}`)

## Directory structure
- `latex`: Latex source code
- `tools`: Supporting tools, including a word count checker

## LaTeX Structure

### Main Document
- `latex/main.tex`: Main paper source
- `latex/IEEEcsmag.cls`: IEEE Computer Society magazine class
- `latex/references.bib`: Bibliography entries
- `latex/figs/`: Figures directory

### Key LaTeX Conventions
- Uses `IEEEcsmag` document class
- Citations use `[super]{cite}` package for superscript format
- Biographies use `IEEEbiography` environment
- Section numbering disabled (`\setcounter{secnumdepth}{0}`)
- **Always use `\ref{}` for figure/table numbers**: Never hardcode "Figure 1", use `Figure~\ref{fig:label}` instead
- Use non-breaking space (`~`) before `\ref{}` to prevent line breaks between "Figure" and the number

## Development Guidelines and Conventions

- Always run `./check_word_count.sh` after significant changes
- Update `references.bib` for new citations
- Latex comments (%) in `main.tex` typically refer to TODOs 
- File `Notes.md` is a scratchpad with additional ideas for the paper

### Check Word Count (tool)

```bash
./check_word_count.sh
```
This runs the IEEE Software word count checker, which validates:
- Abstract ≤ 150 words
- Total ≤ 4200 words (including 250 words per figure/table/code block)
- References ≤ 15
- Exit code 0 = pass, 2 = fail

To manually run the word count check tool:
```bash
python3 tools/ieeesw_wordcheck.py latex/main.tex --expand-inputs
python3 tools/ieeesw_wordcheck.py latex/main.tex --expand-inputs --json
```

### Build PDF
Use latexmk:
```bash
cd latex
latexmk -pdf main.tex
```