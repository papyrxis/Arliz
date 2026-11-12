# Stage 01 — Data and Physical Representation

Stage 01 is the opening stage of **Volume I — Zero to Bit**. Its conceptual path moves from the nature of data, through representation, to the physical states and signals that can carry representations.

## Companion booklet

The same three-chapter foundation is also being developed as a standalone bilingual booklet:

**[01 — What Data Is, and Why It Must Become Physical](https://github.com/papyrxis/papers/tree/main/booklets/01-what-data-is-and-why-it-must-become-physical)**

The booklet is maintained in [Papyrxis Papers](https://github.com/papyrxis/papers), which owns its independent editions, front matter, bibliography, publication metadata, and PDF build. It is a companion publication—not a remote source that this repository downloads during a build.

| ARLIZ Stage 01 | Companion booklet | Shared subject |
|---|---|---|
| [Chapter 01](./chapter01/chapter01.tex) | [Chapter 01 (FA)](https://github.com/papyrxis/papers/blob/main/booklets/01-what-data-is-and-why-it-must-become-physical/fa/chapters/chapter01.tex) · [Chapter 01 (EN)](https://github.com/papyrxis/papers/blob/main/booklets/01-what-data-is-and-why-it-must-become-physical/en/chapters/chapter01.tex) | The nature of data |
| [Chapter 02](./chapter02/chapter02.tex) | [Chapter 02 (FA)](https://github.com/papyrxis/papers/blob/main/booklets/01-what-data-is-and-why-it-must-become-physical/fa/chapters/chapter02.tex) · [Chapter 02 (EN)](https://github.com/papyrxis/papers/blob/main/booklets/01-what-data-is-and-why-it-must-become-physical/en/chapters/chapter02.tex) | The philosophy of representation |
| [Chapter 03](./chapter03/chapter03.tex) | [Chapter 03 (FA)](https://github.com/papyrxis/papers/blob/main/booklets/01-what-data-is-and-why-it-must-become-physical/fa/chapters/chapter03.tex) · [Chapter 03 (EN)](https://github.com/papyrxis/papers/blob/main/booklets/01-what-data-is-and-why-it-must-become-physical/en/chapters/chapter03.tex) | From abstract representation to physical signal |

The correspondence is conceptual and chapter-level. It does not promise line-for-line identity: the booklet is an independently edited work and may use a different order, examples, depth, or presentation.

## Source and build boundaries

- **ARLIZ owns the Volume I text.** Its chapter files remain the sources compiled into the English ARLIZ volume.
- **Papers owns the standalone booklet.** Its Persian and English editions, references, and publication files are maintained there.
- Do not replace ARLIZ chapters wholesale merely because the companion booklet is completed. Review substantive changes and adapt only the material that belongs in the Volume I reading path.
- Do not use a remote GitHub URL with LaTeX `\\input`, or add the Papers repository as a Git submodule just to share these chapters. That would couple the Volume I build to another repository and its checkout or network state. The current link keeps both publications independently buildable.
- When a shared concept changes materially, review the corresponding chapter in the other repository and make an intentional editorial update. Preserve each publication's own structure, language, references, and typesetting conventions.

## Editorial status

This is a work-in-progress companion relationship. The public Papers tree may lag behind the author's local draft; in particular, the Chapter 03 sources are not yet a completed publication. Do not treat this link as evidence that a finished booklet PDF or a synchronized release is available.

Once the booklet is ready for publication, update this note with its stable release/PDF link. Keep this source link as the living editorial reference.
