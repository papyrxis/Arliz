# Workflows

Commands for building, validating, and publishing Arliz.

For repository boundaries, see ARCHITECTURE.md. For content placement, see VOLUMES.md.

## Prerequisites and setup

- Python 3.10+ and pip.
- TeX Live with pdflatex, latexmk, Biber, and the packages in .ci/locks/texlive-packages.ubuntu.lock.
- GNU Make, Git, and Bash.
- gix and psx for branch flow, versioning, and quality checks.

Clone the repository and install its locked Python dependencies:

~~~sh
git clone https://github.com/papyrxis/Arliz.git
cd Arliz
python3 -m pip install -r .ci/locks/python-requirements.lock
~~~

The lock installs papyrxis-workspace==0.5.1 from its immutable GitHub release wheel. Do not initialize a Workspace submodule or install an editable Workspace checkout.

## CI toolchain versions and caches

CI uses the reviewed version pins in .ci/locks/go-tools.lock for Gix and PSX. The file content is part of the Go cache key, together with the resolved Go version; a cache hit restores the command binaries, Go modules and compiler cache instead of downloading and compiling the tools again.

The TeX package set is listed in .ci/locks/texlive-packages.ubuntu.lock. Pipeline keys its apt archive cache from that manifest, runner OS and architecture. Change the manifest deliberately when the build needs another TeX package. The first cold GitHub-hosted run still needs to install TeX Live; matching downloaded archives can be reused by later runs.

The shared Pipeline action also accepts latex-setup-mode: verify for a pre-provisioned runner. It checks the required commands and TeX packages without running apt. Use that mode only on a trusted, persistent runner that already contains the complete manifest; do not expose a persistent self-hosted runner to untrusted public pull requests.

The Python build dependency lock also keys the pip download cache. Update it deliberately when Workspace changes, and keep the lock compatible with the package metadata.

## Building

~~~sh
make build       # generate and build all three volumes
make vol1        # build only Volume I
make vol2        # build only Volume II
make vol3        # build only Volume III
~~~

Each volume is generated from main.tex plus its configs/volumes/volN.conf file. Temporary generated entry points are written under .generated/volN/main.tex; Workspace compiles them using the project root as working directory.

PDFs are written to independent Workspace output directories:

~~~text
build/
├── vol1/en/ARLIZ_Zero_to_Bit_Volume_1.pdf
├── vol2/en/ARLIZ_Silicon_Horizon_Volume_2.pdf
├── vol3/en/ARLIZ_Array_Odyssey_Volume_3.pdf
└── manifest.json
~~~

The manifest records each document/edition, the source hash, output path, PDF size, and SHA-256. make build builds all configured volumes and verifies the complete manifest. Individual make volN targets build and verify only that volume, so they can be used before the other volumes exist.

## Verify and test

Run these after a successful full build:

~~~sh
make verify       # Workspace manifest/hash verification + Arliz volume checks
make test         # unit tests followed by full verification
make doctor       # check local toolchain, Workspace, gix, and psx
~~~

A partial build cannot pass full make verify: every volume must have a successful manifest record and a valid PDF at its configured output path.

## Volume front matter

The shared title, copyright and author pages are required for every volume. The volume-specific cover, acknowledgments, preface and introduction files are optional; the template includes them only when the corresponding source file exists. This allows a volume to compile while its editorial front matter is still being written, without committing empty placeholder files.

When a cover or other front-matter section is ready, add it under frontmatter/volN/; it will be included automatically on the next build.

## Generate without compiling

~~~sh
make generate-vol1
make generate-vol2
make generate-vol3
~~~

Generated files in .generated/ are build inputs. Do not edit them directly.

## Cleaning

~~~sh
make clean
make clean-vol1
make clean-vol2
make clean-vol3
~~~

Workspace removes the selected document outputs and reconciles the manifest; the Arliz cleanup adapter removes its generated TeX entry point. A full clean removes all generated volume outputs.

## Git flow and versioning

The repository follows the main / develop flow defined in .gix/config.

~~~sh
gix doctor
gix feature start improve-volume-i
# make changes and commit
gix feature finish
~~~

Inspect the current version with:

~~~sh
make version
~~~

Before using make bump, review the existing tags. The historical tag v1.0.0-beta-Volume_I contains an underscore and is not a Gix-compatible SemVer tag. The guard script intentionally blocks version bumps while a SemVer-shaped incompatible tag remains. Do not rewrite or delete the historical tag automatically; decide on a normalized replacement tag in a separate release decision.

Once the tag history is normalized:

~~~sh
make bump LEVEL=patch
make push TAGS=1
~~~

Alternatively, create a reviewed explicit tag:

~~~sh
make tag RELEASE_VERSION=v1.2.0
make push TAGS=1
~~~

Pushing to main updates the rolling latest-pre-release. Pushing a compatible version tag invokes the versioned release workflow. Both workflows call the same reusable Pipeline build.

## Adding a chapter

1. Decide which volume owns the content (see VOLUMES.md).
2. Add the chapter source under the matching volumes/volN/ directory.
3. Add its input reference to the volume's master file.
4. Run make volN and confirm that the output PDF passes verification.
