# ARLIZ

**Arrays, Reasoning, Logic, Identity, Zero**

Arliz is a continuous book about arrays, organized as three independently buildable volumes.

| Volume | Title | Focus |
|---|---|---|
| I | *Zero to Bit* | Information representation, encoding, and Boolean foundations |
| II | *Silicon Horizon* | The hardware that turns encoded bits into computation |
| III | *Array Odyssey* | Arrays, their algorithms, and their applications |

Each volume is compiled to its own PDF. The source content remains in this repository; shared LaTeX components and workspace tooling come from the [Papyrxis Workspace](https://github.com/papyrxis/workspace) submodule.

## Build

Clone with the shared workspace:

```sh
git clone --recurse-submodules https://github.com/papyrxis/Arliz.git
cd Arliz
python3 -m pip install -e workspace
make build                 # all three volumes
make vol1                  # one volume
make test                  # tests and PDF verification (after make build)
make clean
```

Requirements include Python 3.10+, PyYAML, GNU Make, Bash, and TeX Live with `latexmk`, `pdflatex`, and Biber.

## Shared engineering tools

- [Workspace](https://github.com/papyrxis/workspace) provides reusable LaTeX components and publishing utilities.
- [Pipeline](https://github.com/m-mdy-m/pipeline) runs the shared LaTeX CI preset.
- [gix](https://github.com/m-mdy-m/gix) manages branch flow and semantic versioning.
- [psx](https://github.com/m-mdy-m/psx) checks repository quality.

Every push to `main` updates the rolling [latest pre-release](https://github.com/papyrxis/Arliz/releases/tag/latest-pre-release). Versioned tags publish stable or explicitly marked prereleases.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/WORKFLOWS.md](docs/WORKFLOWS.md), and [docs/VOLUMES.md](docs/VOLUMES.md).

## Contributing

Corrections, clarifications, examples, diagrams, and chapters are welcome. Start with [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

## License

- Book content is licensed under CC BY-SA 4.0; see [CONTENT-LICENSE.md](CONTENT-LICENSE.md).
- Build scripts and tooling are MIT-licensed; see [LICENSE](LICENSE).
