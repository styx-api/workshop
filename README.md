# NiWrap hands-on workshop

A 90-minute hands-on workshop on using [NiWrap](https://github.com/styx-api/niwrap), the Styx-generated Python wrappers for FSL, ANTs, AFNI, FreeSurfer, MRtrix3 and other neuroimaging tools. Audience: researchers with basic Python.

- Attendees: [`SETUP.md`](SETUP.md), before the day. Get the materials with `git clone https://github.com/styx-api/workshop.git niwrap-workshop` or as a [ZIP](https://github.com/styx-api/workshop/archive/refs/heads/main.zip).
- Facilitators: [`FACILITATOR.md`](FACILITATOR.md) for timing, failure points, the no-Docker fallback and demo commands.

## Contents

| Path | |
|---|---|
| `slides/workshop.md` | Marp slide deck with speaker notes |
| `notebooks/01_first_calls.ipynb` | Python call vs. CLI command, BET, autocomplete, chaining (10–25 min) |
| `notebooks/02_runners.ipynb` | Local, Docker, DryRunner, `use_auto()`, where files go (25–35 min) |
| `notebooks/03_pipeline_starter.ipynb` | Hands-on: extend the Styx book's anat_preproc into a multi-subject pipeline, with TODOs (35–65 min) |
| `notebooks/03_pipeline_solution.ipynb` | One possible solution |
| `snakemake/` | The same pipeline idea in Snakemake, from niwrap-workflow-examples (65–75 min) |
| `scripts/fetch_data.py` | OpenNeuro ds000001 sub-01..03 T1w (BIDS) + MNI152NLin2009cAsym from TemplateFlow, into `data/` |
| `scripts/prepull_images.sh` | Pulls the two container images the pipeline uses |
| `scripts/smoke_test.py` | Checks data, Docker, images, and runs FSL + ANTs once |

Each notebook starts with `RUNNER = "auto"` (`niwrap.use_auto()`: Docker if available). Set it to `"dry"` to build and check commands without running them.

## Pinned versions

`pyproject.toml` pins NiWrap and the runner packages; `uv.lock` pins everything else. Python 3.13 (`.python-version`; ≥3.12 works).

| Package | Version |
|---|---|
| niwrap (+ niwrap-fsl, niwrap-ants, ... per-toolbox packages) | 1.1.0 |
| styxkit | 0.1.0 |
| styxdefs | 0.7.0 |
| styxdocker | 0.8.0 |
| styxsingularity | 0.9.0 |
| styxpodman | 0.3.0 |
| styxgraph | 0.7.0 |
| styxcontainer-common (transitive) | 0.3.0 |
| snakemake | 9.27.0 |
| jupyterlab / ipykernel | 4.6.4 / 7.4.0 |
| nilearn / nibabel / matplotlib | 0.13.1 / 5.4.2 / 3.11.2 |

Container images (defaults baked into niwrap 1.1.0, both linux/amd64 only):

| Image | Download | On disk |
|---|---|---|
| `brainlife/fsl:6.0.4-patched2` | 7.1 GB | 23.5 GB |
| `antsx/ants:v2.5.3` | 0.1 GB | 0.6 GB |

The RBC demo runs separately through `uvx` at `childmindresearch/rbc@9eaf3ac`, which resolves `niwrap==0.9.6` (RBC pins `<1.0`). Its anatomical stage uses the two images above plus `afni/afni_make_build:AFNI_24.2.06` (0.8 GB download, 3.1 GB on disk); only the presenter needs it.

## Slides

Marp: one Markdown file that renders on GitHub, speaker notes as HTML comments, preview and export (HTML, PDF, PPTX) from VS Code or `npx`, nothing else to install. Quarto's advantage is executing code in slides, which isn't needed here: slide code is copied from the executed notebooks.

```bash
npx @marp-team/marp-cli@4.1.2 slides/workshop.md -o slides/workshop.html   # presenter view: press P
npx @marp-team/marp-cli@4.1.2 slides/workshop.md --pdf
npx @marp-team/marp-cli@4.1.2 slides/workshop.md --pptx -o slides/workshop.pptx
```

`slides/workshop.pptx` is that export: each slide is an image, speaker notes are PowerPoint notes. Edit `workshop.md` and re-export rather than editing the `.pptx`.

## Sources

Code and APIs come from these, checked against the installed packages:

- Styx book, [niwrap.dev/styxbook](https://niwrap.dev/styxbook/) (`styx-api/styxbook` @ `bf8cea6`): Getting started, Runners, I/O, examples `anat_preproc`, `dynamic_runners`, `mermaid`
- [`styx-api/niwrap-workflow-examples`](https://github.com/styx-api/niwrap-workflow-examples) @ `869f772`: the Snakemake example in `snakemake/`
- [`childmindresearch/rbc`](https://github.com/childmindresearch/rbc) @ `9eaf3ac`: RBC demo
- [`styx-api/niwrap`](https://github.com/styx-api/niwrap) README: tool coverage numbers on the slides

Where the book and NiWrap 1.1.0 disagree, the material follows the installed version. Differences are listed at the end of `FACILITATOR.md`.

## Figure credits

| `slides/img/` | Source |
|---|---|
| `cli_structure.jpg`, `styx_layers.png` | Styx preprint, Figs. 1 and 4 ([doi:10.1101/2025.07.24.666435](https://doi.org/10.1101/2025.07.24.666435), CC-BY) |
| `before_after.png`, `flower.png` | OHBM 2026 poster "A Collaborative Infrastructure Around Shared Tool Interfaces for Neuroimaging" |
| `vscode_hover.png` | OHBM 2024 Styx poster |
| `rbc_pipeline.svg` | [`childmindresearch/rbc`](https://github.com/childmindresearch/rbc) `docs/pipeline_flow.svg` @ `9eaf3ac` |
| `rbc_harmonization.png` | [reprobrainchart.github.io](https://reprobrainchart.github.io/) site banner |
| `nipype_logo.svg` | [`nipy/nipype`](https://github.com/nipy/nipype) `doc/_static/snakebrain-nipype.svg` |
| `snakemake_dag.png` | `snakemake --dag mermaid-js` on `snakemake/Snakefile`, rendered with mermaid-cli |
| `bet.png`, `fast.png`, `mni_subjects.png`, `rbc.png` | Outputs of the notebooks and the RBC run |
| `repo_qr.png` | Generated with `segno` |
| `cmi_logo*.png` | Child Mind Institute PowerPoint template (2023); slide colors and Arial follow the same template |
