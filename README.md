# ARLIZ

**Arrays, Reasoning, Logic, Identity, Zero**

**Arliz** is a book about arrays. Not just how to use them — but how they *work*, where they come from, and why they matter.

It started as a personal attempt to understand arrays beyond syntax and surface-level use: *what is an array, really?* Following that question seriously turned a familiar programming topic into a much larger inquiry — one that runs from a voltage difference across a transistor all the way to tensor cores and quantum state vectors.

That path is long enough that it no longer fits in a single book. Arliz is organized as **one continuous work in three volumes**, each a complete stage of the same journey, readable on its own but part of one larger whole.

## The Three Volumes

| Volume | Title | Status | Covers |
|---|---|---|---|
| **I** | *Zero to Bit* | Living draft (78 chapters, 17 stages) | How information is encoded at all, starting one level below a transistor: charge, current, voltage, and circuit fundamentals; the semiconductor physics and CMOS switching that turn a voltage into a bit; Boolean algebra as pure mathematics; number systems, integers, and floating point; characters and Unicode; endianness; bitwise operations; memory alignment; pointers; error detection and correction; media encodings; and serialization and compression. |
| **II** | *Silicon Horizon* | In progress (129 chapters, 12 stages) | The hardware that turns encoded bits into computation, picking up exactly where Volume I's Boolean algebra leaves off: logic gate implementation, arithmetic and sequential circuits, memory cells and the full memory hierarchy, instruction set architectures, pipelining and out-of-order execution, virtual memory, I/O and interrupts, multicore/SIMD/GPU execution, and power, thermal, and security concerns. |
| **III** | *Array Odyssey* | In progress (184 chapters, 7 stages) | Arrays themselves, in full: the mathematical theory and memory layout, every major variant (dynamic, multidimensional, sparse, bit arrays, ring buffers), searching and sorting, in-place manipulation patterns, vectorized operations, the classic data structures and algorithms built on top of arrays, parallel and distributed array processing, and a representative — not exhaustive — tour of the domains where arrays do real work. |

Each volume assumes the ones before it: Volume II assumes the representational vocabulary built in Volume I, and Volume III assumes both. The boundary between Volume I and Volume II is deliberate — Volume I stops at "a transistor can hold one bit, and bits compose into Boolean algebra"; Volume II starts there and builds upward, rather than re-deriving semiconductor physics or CMOS. See [`docs/VOLUMES.md`](./docs/VOLUMES.md) for the full breakdown of what each volume contains and how they connect.

## Read the Book

Each volume compiles to its own standalone PDF, named:

```
<YEAR>_ARLIZ_<Volume Title>_Volume_<N>.pdf
```

For example, Volume I currently builds as `2026_ARLIZ_Zero_to_Bit_Volume_1.pdf`.

- [Browse LaTeX source](./volumes/)
- Compiled PDFs are published under [Releases](https://github.com/papyrxis/Arliz/releases) and on the [project site](https://github.com/papyrxis/Arliz/tree/main/docs)

## Contributing

Contributions — corrections, clarifications, new examples, diagrams, or whole chapters — are welcome. Start with:

- [`docs/CONTRIBUTING.md`](./docs/CONTRIBUTING.md) — how to report issues, open PRs, and the editorial/LaTeX standards
- [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) — how the repository, build system, and workspace presets fit together
- [`docs/WORKFLOWS.md`](./docs/WORKFLOWS.md) — concrete day-to-day commands for building, generating chapters, and cleaning artifacts
- [`docs/VOLUMES.md`](./docs/VOLUMES.md) — what each volume covers, so you know where new content belongs

## License

- **Book content** (chapters, explanations, diagrams, prose) is licensed under **CC BY-SA 4.0**.
- **Source code, build scripts, and LaTeX tooling** are licensed under the **MIT License** (see [`LICENSE`](./LICENSE)).

See [`frontmatter/copyright.tex`](./frontmatter/copyright.tex) for the full copyright and citation notice.