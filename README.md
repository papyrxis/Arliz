# ARLIZ

**Arrays, Reasoning, Logic, Identity, Zero**

Arliz is a continuous book about arrays, organized as three independently buildable volumes.

| Volume | Title | Focus |
|---|---|---|
| I | *Zero to Bit* | Information representation, encoding, and Boolean foundations |
| II | *Silicon Horizon* | The hardware that turns encoded bits into computation |
| III | *Array Odyssey* | Arrays, their algorithms, and their applications |

Each volume remains an independent Workspace document. Arliz owns all editorial sources and project-specific LaTeX configuration; the shared publishing engine is installed as the pinned papyrxis-workspace Python package. A Workspace checkout or Git submodule is not required.

## Build

~~~sh
git clone https://github.com/papyrxis/Arliz.git
cd Arliz
python3 -m pip install -r .ci/locks/python-requirements.lock
make build                 # all three volumes
make vol1                  # one volume
make test                  # tests and manifest/PDF verification
make clean
~~~

Workspace is pinned to the immutable v0.5.1 wheel in .ci/locks/python-requirements.lock. The build generates temporary TeX entry points under .generated/, then delegates compilation, isolated outputs, the SHA-256 manifest, and PDF verification to Workspace.

Outputs are kept separate:

- build/vol1/en/ARLIZ_Zero_to_Bit_Volume_1.pdf
- build/vol2/en/ARLIZ_Silicon_Horizon_Volume_2.pdf
- build/vol3/en/ARLIZ_Array_Odyssey_Volume_3.pdf

Requirements include Python 3.10+, PyYAML, GNU Make, Bash, and TeX Live with latexmk, pdflatex, and Biber.

## Shared engineering tools

- [Workspace](https://github.com/papyrxis/workspace) provides the reusable publishing engine and shared LaTeX components.
- [Pipeline](https://github.com/m-mdy-m/pipeline) runs the shared LaTeX CI preset.
- [gix](https://github.com/m-mdy-m/gix) manages branch flow and semantic versioning.
- [psx](https://github.com/m-mdy-m/psx) checks repository quality.

Every push to main updates the rolling [latest pre-release](https://github.com/papyrxis/Arliz/releases/tag/latest-pre-release). Versioned tags publish stable or explicitly marked prereleases.

See docs/ARCHITECTURE.md, docs/WORKFLOWS.md, and docs/VOLUMES.md.

## Contributing

Corrections, clarifications, examples, diagrams, and chapters are welcome. Start with docs/CONTRIBUTING.md.

## License

- Book content is licensed under CC BY-SA 4.0; see CONTENT-LICENSE.md.
- Build scripts and tooling are MIT-licensed; see LICENSE.
