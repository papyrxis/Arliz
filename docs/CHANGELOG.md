# Changelog

All notable changes to **Arliz** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
as far as a living, multi-volume work allows: a release marks a milestone in the
*structure, tooling, or documentation* of the project and/or in the *content* of
one or more volumes -- it does not imply that any volume is "finished."

Each volume continues to evolve independently between tagged releases. Compiled
PDFs are named `<YEAR>_ARLIZ_<Volume_Title>_<N>.pdf` and published as assets on
the corresponding [GitHub Release](https://github.com/papyrxis/Arliz/releases).

## [Unreleased]

### Changed -- De-duplication and scope reduction across all three volumes

> **Why:** an outside read-through flagged the project as feeling scattered,
> with abstraction level swinging between chapters and the same ground
> covered more than once. Auditing the actual chapter outlines confirmed
> both problems concretely (not just as an impression) and this pass fixes
> them. Total chapter count across the three volumes goes from **677 to
> 393** (Volume I: 81 -> 80, Volume II: 132 -> 129, Volume III: 464 -> 184).

- **Volume I / Volume II seam:** Volume I's Stage 4 (semiconductor physics,
  doping, the P-N junction, the MOSFET, CMOS technology) and Volume II's
  former Stage 1 opening ("Semiconductor Physics Foundations," "MOSFET
  Transistors," "CMOS Logic Fundamentals") covered the same ground twice.
  Removed the three duplicate chapters from Volume II; Volume II's Stage 1
  now starts at "Logic Gate Implementation," composing the gates Volume I
  already established rather than re-deriving the transistor.
  - Also removed Volume I's "Logic Gate Families and Circuit Building"
    chapter (CMOS realization, fan-in/fan-out, propagation delay) -- that
    circuit-implementation content is Volume II's job; Volume I's Stage 6
    now covers Boolean algebra purely as mathematics.
  - Merged `volumes/vol1/vol-1.draft.tex` (Stages 2-17, previously a
    separate draft not yet wired into the build) into `volumes/vol1/vol1.tex`
    as the single source of truth. The old draft is kept for reference at
    `volumes/vol1/drafts/_archived/vol-1.draft.tex.superseded`.
- **Volume III scope:** restructured from 464 chapters (7 sections, A-G) to
  184 chapters (7 stages, renamed for consistency with Volumes I/II's
  "Stage" terminology). The cut followed one rule throughout: for every
  chapter, "after this, how much closer is the reader to actually
  understanding and using arrays?" Three kinds of cuts followed from that:
  - **Exact duplicates removed:** "Cache-Oblivious Algorithms Revisited,"
    "Streaming Algorithms," and "Probabilistic Data Structures Summary"
    (formerly in the applications section) fully duplicated chapters
    already present earlier in the same volume; removed in favor of the
    earlier treatment. "Broadcasting Semantics" in the applications section
    duplicated the broadcasting chapter in the array-operations stage;
    removed likewise.
  - **Minor variants merged into one comparative chapter:** e.g. five
    specialized search algorithms (interpolation, exponential, ternary,
    jump, Fibonacci) became one "Specialized Search Algorithms" chapter;
    nine hash-table chapters became five; twenty neural-network chapters
    became six. This is the majority of the reduction.
  - **Applications compressed, not eliminated:** quantum computing,
    bioinformatics, neuromorphic/analog computing, DNA storage, and similar
    domains each had multiple dedicated chapters; each is now exactly one
    consolidated survey chapter. The domains are still represented; the
    encyclopedic depth is not.
  - Old 464-chapter outline kept for reference at
    `volumes/vol3/_archived/vol3.tex.superseded-464ch`.
- Updated `docs/VOLUMES.md` to match: Volume II's description no longer
  claims semiconductor physics, and Volume III's description no longer
  claims "in full" coverage.
- Updated `frontmatter/vol1/Introduction.tex` to state the Volume I/II
  boundary explicitly for readers, not just in source comments.

### Fixed -- Fabricated citations removed from Volume I, Chapter 1

> Four entries in `references/arliz.bib` -- `ratzky2005`, `mccal2004`,
> `tansen2013`, `pippenborg2011` -- could not be verified to exist anywhere
> under any search. Each had a fabricated co-author, title, and publisher;
> `pippenborg2011` additionally carried a fabricated DOI. This is the
> classic citation-hallucination failure mode of AI-assisted writing: a
> generically plausible claim gets a confident-sounding name and year
> attached with no real source behind it. (`ratzky2005` in particular looks
> like a corrupted duplicate of the real, correctly-cited `ratzan2004` a
> few lines later in the same file.)

- Removed all four fabricated entries from `references/arliz.bib`, with a
  note in the file explaining why and a reminder to verify any future
  AI-suggested citation before adding it.
- Removed the corresponding six `\autocite{}` calls from
  `volumes/vol1/chapter01/chapter01.tex` and lightly re-worded the
  surrounding sentences so they stand as the author's own observations
  (which is what they always were) rather than uncited-but-still-citing
  claims.
- **Not yet done:** the other nine entries in `arliz.bib` look real on
  inspection (Shannon, Knuth, Pierce, Floridi, Zins, Ackoff, Ratzan,
  Walliman, Rob/Morris/Coronel, UNESCO, Marx, Webster's, OED) but have not
  been individually re-verified here. Recommended before any chapter
  ships: a pass that confirms every citation in this file actually exists
  and says what it's cited as saying.

## [1.0.0-beta-Volume_I] - 2026-06-15

> **This is a structural release, not a content release.** No chapter prose has
> been written for any volume yet -- every chapter in `parts/part01/`,
> `parts/part02/`, and `parts/part03/` currently exists only as a `\chapter{}`
> title with a short, comma-separated outline of the topics it will eventually
> cover. What this release delivers is the complete reorganization of Arliz from
> a single six-part book into three independent, continuously-buildable volumes,
> together with the build pipeline, templates, front matter, documentation, and
> website needed to support that structure going forward. "Volume I" appears in
> the version tag because its front matter (preface, introduction,
> acknowledgments, cover) and build configuration are the most complete of the
> three, and `vol1.pdf` is the first volume to have been built end-to-end as a
> test of the new pipeline.

### Changed -- Restructuring: six parts into three volumes

- Reworked the project from a single book organized into "Part 1" through
  "Part 6" into **three standalone volumes**, each compiling to its own PDF:
  - **Volume I -- *Zero to Bit*** (`parts/part01/part01.tex`, `volumes/vol1.conf`)
    -- representation and encoding, from a voltage difference to bits, numbers,
    characters, and serialization.
  - **Volume II -- *Silicon Horizon*** (`parts/part02/part02.tex`, `volumes/vol2.conf`)
    -- the hardware that executes arrays: logic gates, memory, ISAs, pipelines,
    SIMD, GPUs, and interconnects.
  - **Volume III -- *Array Odyssey*** (`parts/part03/part03.tex`, `volumes/vol3.conf`)
    -- arrays themselves: theory, memory layout, data structures, algorithms,
    parallel/distributed processing, and applications.
- Redistributed the planned content of the former "Part 4 -- Data Structures &
  Algorithms", "Part 5 -- Parallelism & Systems", and "Part 6 -- Synthesis &
  Frontiers" into Volumes I-III, at the points in the voltage-to-tensor
  narrative where each topic naturally belongs (documented as `MERGE NOTES`
  comments at the top of each `partXX.tex`):
  - NUMA architecture, SIMD/vector ISA chapters, GPU architecture/execution/
    memory/programming models, and TPU systolic arrays now sit in **Volume II**,
    immediately after the single-unit hardware topics they extend.
  - Stacks, queues, heaps, hash tables and probabilistic structures, strings and
    pattern matching, suffix structures, tries, graphs, range-query structures
    (segment tree, Fenwick tree, sparse table), dynamic programming, divide &
    conquer, greedy algorithms, backtracking, and streaming/amortized analysis
    now sit in **Volume III** as "structures and algorithms built on arrays".
  - Concurrency fundamentals, performance laws, threads/thread pools, OpenMP,
    synchronization primitives, lock-free structures, GPU array algorithms
    (sort/reduce/scan), and distributed array processing (MPI, MapReduce,
    Spark, PGAS, consensus) now sit in **Volume III** as a "parallel and
    distributed array processing" section.
  - Tensors and ML array operations, attention/transformers, linear algebra
    (BLAS/LAPACK), scientific computing and FFT, image/audio/video/signal
    processing, geospatial and bioinformatics arrays, quantum state vectors,
    array programming languages, and emerging array hardware/paradigms now sit
    in **Volume III** as the closing "arrays in science, machine learning, and
    beyond" section.
- Volume II's outline intentionally **excludes** the consumer-hardware
  repair/diagnostic chapters (motherboard repair, PSU diagnostics, mobile
  device teardown, soldering, etc.) that existed in the old Part 2 plan.
- Volume III's outline **drops** the memory/storage hardware-testing and
  diagnostic chapters (March algorithms for RAM testing, SMART attributes,
  etc.) that were appended to the end of the old Part 3 plan.
- Rewrote `README.md` to describe the three-volume structure, the
  dependency order between volumes, pointers to the new `docs/` guides, and
  the dual-license model (CC BY-SA 4.0 for content, MIT for code/tooling).
- Rewrote the project website (`docs/index.html`, `docs/style.css`,
  `docs/script.js`): new hero section with the ARLIZ acronym breakdown
  (Arrays, Reasoning, Logic, Identity, Zero), a "One Journey, Three Volumes"
  section, live GitHub stats and a contributors grid pulled from the GitHub
  API, and a community/contribution section.

### Added -- Build system and tooling

- New shared LaTeX template `main.tex`, instantiated once per volume via
  token substitution (`@PDF_TITLE@`, `@PDF_TITLE_FRONT@`, `@PDF_COVER_TITLE@`,
  `@PDF_SUBJECT@`, `@PDF_KEYWORDS@`, `@FRONTMATTER_DIR@`, `@MAIN_FRONTMATTER@`,
  `@PARTS@`, `@BACKMATTER@`).
- New per-volume configuration files `volumes/vol1.conf`, `volumes/vol2.conf`,
  and `volumes/vol3.conf`, each describing that volume's PDF metadata, front
  matter directory, list of `\part{}`/`\input{}` files, back matter files,
  volume number/title, and cover image.
- New generation/build/clean scripts under `scripts/volumes/`:
  - `generate.sh <volN>` -- produces `<YEAR>_ARLIZ_<Title>_<N>.tex` from
    `main.tex` + the volume's `.conf` file, for manual compilation (e.g. in
    TeXstudio).
  - `build.sh <volN|all>` -- generates and compiles a volume (or all volumes)
    with `latexmk` (pdflatex + biber, multiple passes), producing
    `build/<YEAR>_ARLIZ_<Title>_<N>.pdf`.
  - `clean.sh` -- removes all generated top-level volume `.tex` files and
    `build/`.
- New top-level `Makefile` with targets: `vol1`, `vol2`, `vol3`, `volumes`,
  `generate-vol1`/`generate-vol2`/`generate-vol3`, `clean-vol1`/`clean-vol2`/
  `clean-vol3`, `clean-vols`, `sync`, `build`, `watch`, `part`, `chapter`,
  `cover`, `test`, `version`, and `help`.
- First end-to-end build of **Volume I** (`vol1.pdf`) produced as a test of the
  new modular pipeline.
- Regenerated the per-volume `.tex` and `.pdf` outputs for all three volumes
  against the finalized `volumes/*.conf` files and directory layout.

### Added -- Front matter and shared content

- New per-volume front matter for Volume I under `frontmatter/vol1/`:
  `cover.tex`, `preface.tex`, `Introduction.tex`, and `acknowledgments.tex`.
- New shared front matter: `frontmatter/title.tex` (title page),
  `frontmatter/copyright.tex` (copyright notice and dual-license terms,
  preferred citation, and contact information), and `frontmatter/about_author.tex`
  (a new "About the Author" chapter, including the author photo).
- New shared back matter content (glossary placeholder, bibliography section,
  and a closing "Reflections at the End" / author's notes section).
- Added the `wrapfig` package to the graphics configuration
  (`.pxis/components/graphics.tex` and `configs/graphics.tex`) to support the
  author-photo layout used in "About the Author".
- Added and customized the `hyperref` setup
  (`.pxis/components/hyperref.tex`) with PDF metadata (title, author, subject,
  keywords) and link styling, wired up via `\PDFTitle`, `\PDFAuthor`, and
  related macros in `main.tex`.

### Added -- Documentation

- New `docs/ARCHITECTURE.md` explaining the repository layout, the
  template-plus-per-volume-config pattern, the volume config variables, and
  how the three volumes are produced from one shared source tree.
- New `docs/VOLUMES.md` describing what each volume covers, the one-directional
  dependency order between volumes (I -> II -> III), and where new chapters
  should be added.
- New `docs/WORKFLOWS.md` with concrete day-to-day commands for building,
  generating, and cleaning each volume, plus a troubleshooting section.
- New `docs/CONTRIBUTING.md` covering local setup, issue reporting (using the
  templates below), the pull-request process, branching strategy, semantic
  commit-message conventions, source-documentation rules, LaTeX coding
  standards, and editorial guidelines.
- New `docs/CHANGELOG.md` (this file).
- New GitHub issue templates under `.github/ISSUE_TEMPLATE/`: `bug_report.yml`,
  `feature_request.yml`, `documentation_update.yml`, `discussion_ideas.yml`,
  and `general_inquiry.yml`, adapted to Arliz's volume/part terminology and the
  two-digit `book/parts/partNN/` referencing convention.
- New `.github/ISSUE_TEMPLATE/config.yml` pointing contributors to the README
  and `docs/CONTRIBUTING.md` instead of generic placeholder links.
- New `.github/PULL_REQUEST_TEMPLATE.md` with a structured checklist covering
  LaTeX content changes, macros, figures/tables, structural changes, and build
  verification steps (`xelatex`/`biber` passes).

### Added -- Repository hygiene

- New `.gitignore` covering LaTeX build byproducts (`*.aux`, `*.log`, `*.out`,
  `*.toc`, `*.bbl`, `*.bcf`, `*.blg`, `*.synctex.gz`, `*.fdb_latexmk`, `*.fls`,
  index/glossary artifacts, etc.), the `build/` and `.backups` directories, and
  generated top-level volume files (`/vol*.tex`, `*_ARLIZ_*.tex`).
- New `.gitattributes` marking `*.tex` files as not linguist-detectable.

### Removed

- Removed "Part 4", "Part 5", and "Part 6" as independent top-level parts of
  the book. No planned content was deleted outright -- it was relocated into
  Volumes I-III and re-outlined as described above.

### Fixed

- Fixed `make watch` not correctly invoking the watch-mode build script.

### Notes -- naming history

- Volume I went through the working title **"BIT GENESIS"** during early
  restructuring before being finalized as **"Zero to Bit"**.
- Volume II was finalized as **"Silicon Horizon"** in the same naming pass.
- Volume III's title, **"Array Odyssey"**, was set as part of the initial
  three-volume split and has not changed since.

[Unreleased]: https://github.com/papyrxis/Arliz/compare/v1.0.0-beta-Volume_I...HEAD
[1.0.0-beta-Volume_I]: https://github.com/papyrxis/Arliz/releases/tag/v1.0.0-beta-Volume_I