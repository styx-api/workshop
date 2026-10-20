# Facilitator guide

90 minutes, two thirds hands-on. Slides: `slides/workshop.md`, speaker notes in the HTML comments. Plan one helper per 10–15 attendees.

## Before the day

- [ ] Send `SETUP.md` a week ahead and again two days before. Ask anyone whose smoke test fails to send you its output.
- [ ] On the presenting laptop, from a fresh clone: `uv sync`, `uv run scripts/fetch_data.py`, `bash scripts/prepull_images.sh`, `uv run scripts/smoke_test.py`. For the RBC demo also `docker pull --platform linux/amd64 afni/afni_make_build:AFNI_24.2.06`.
- [ ] Pre-compute everything you'll show, so no demo waits on a live run:
  ```bash
  uv run jupyter nbconvert --to notebook --execute --output solution_run.ipynb notebooks/03_pipeline_solution.ipynb
  uv run snakemake -s snakemake/Snakefile --cores 3
  uvx --from git+https://github.com/childmindresearch/rbc@9eaf3ac rbc anatomical data/ds000001 \
      -o derivatives/rbc --participant-label 01 --ants-threads 4 --tmp-dir work/rbc
  ```
- [ ] USB stick with `data/` (50 MB) and the images: `docker save brainlife/fsl:6.0.4-patched2 antsx/ants:v2.5.3 | gzip > niwrap-images.tar.gz` (about 7 GB; `docker load -i niwrap-images.tar.gz` takes ~10 min). Venue Wi-Fi won't handle 30 people pulling 7 GB.
- [ ] Slides: *Marp for VS Code* extension, or `npx @marp-team/marp-cli@4.1.2 slides/workshop.md -o slides/workshop.html` (press <kbd>P</kbd> for presenter view), `--pdf` for PDF.

## Timing

| Time | Block | Do | Watch for |
|---|---|---|---|
| 0–10 | Why NiWrap | Slides 1–9. Everyone opens `01_first_calls.ipynb` and runs the setup cell meanwhile. | Failed setup cells. Send a helper; anyone not fixed by minute 10 switches to `RUNNER = "dry"`. |
| 10–25 | First calls | Live-code notebook 01, 2-min autocomplete exercise. The last cell (FAST) takes ~2 min: start it and move to the Runners slides. | VS Code kernel selection. Jupyter autocomplete needs an idle kernel. |
| 25–35 | Runners | Notebook 02. Open `work/02/<id>_0_bet/run.sh` in the file browser. | |
| 35–65 | Pipeline | Slides 22–25, then `03_pipeline_starter.ipynb`. Walk the room. Solution slides 26–28 at ~60 min. | Step 0 takes ~2 min. Run sub-01 first; start the loop only after TODO 4. |
| 65–75 | Snakemake | Repo-root terminal: `-n`, open `snakemake/Snakefile` and `scripts/preprocess.py`, show pre-computed `derivatives/snakemake/`. | A live `--cores 3` run took 4.5 min on the 16-core desktop; longer on laptops, so have results ready. |
| 75–83 | RBC | `rbc anatomical --help`, start the command, open `segmentation.py` and `niwrap.py` on GitHub, show pre-computed `derivatives/rbc/`. | Ctrl+C the live run once the first container starts. |
| 83–90 | Q&A | Last slide; common questions in its notes. | |

Running late? Cut, in order: the autocomplete exercise (demo it instead), the "Where are my files" and "Quieter logs" cells in 02, the live RBC run.

## Measured runtimes

16-core Windows 11 desktop, Docker Desktop (WSL2), one ds000001 subject. Expect 1.5–3× on a 4-core laptop, more on Apple Silicon.

| Step | Time |
|---|---|
| `fslreorient2std`, `robustfov`, `bet` | 2–5 s each |
| `N4BiasFieldCorrection` | 5 s |
| `fast` | ~2 min (up to 4 on a busy machine) |
| Snakemake example, 3 subjects, `--cores 3` | 4.5 min |
| `antsRegistrationSyNQuick.sh`, 1 thread (default) | 5:00 |
| `antsRegistrationSyNQuick.sh`, 4 threads | 1:57 |
| `antsApplyTransforms` | 7 s |
| Notebook 03 solution, all cells (Step 0 + 3 subjects) | 12 min |
| RBC `anatomical`, 1 subject, `--ants-threads 8` | 38 min (brain extraction 12, registration 23; machine was busy with other runs) |

## Likely failures

| Symptom | Cause | Fix |
|---|---|---|
| `FileNotFoundError` (`WinError 2` / `No such file or directory: 'bet'`) on the first tool call | No Docker found, so `use_auto()` fell back to local tools, which aren't installed | Start Docker Desktop and re-run the setup cell, or `RUNNER = "dry"`. `niwrap.resolve_runner()` shows what `use_auto()` will pick. |
| `StyxDockerError` with `error during connect` / `Cannot connect to the Docker daemon` | Docker Desktop stopped after the setup cell ran | Start it and re-run the cell. |
| First call hangs for minutes | Image not pre-pulled; Docker is downloading 7 GB | Wait if the network allows; else USB stick or dry mode. |
| `requested image's platform (linux/amd64) does not match` | Apple Silicon | Harmless. Rosetta makes it faster. |
| ANTs fails with return code 137 | Out of memory in Docker Desktop | Memory ≥ 8 GB, restart Docker. |
| `no space left on device` | FSL image is 23.5 GB unpacked | Free disk. |
| `Input file not found: ".../data/ds000001/..."` | Data not fetched, or notebook not run from `notebooks/` | `uv run scripts/fetch_data.py`; open notebooks normally (Jupyter and VS Code use the notebook's folder). |
| ``StyxValidationError: `infile` must not be None`` | An earlier output wasn't named, so it's `None` | Pass `output_image=` / `out_basename=`. |
| `dc: command not found` from `bet` | `robust_iters=True` (`-R`) fails in the default FSL image | Leave out `-R`; `robustfov` already crops the neck. |
| `NotImplementedError: TODO 2` / `KeyError` in the starter | TODO not done yet | Expected. |
| VS Code shows no `.venv` kernel | Wrong folder opened, or no `uv sync` | Open the repo folder, `uv sync`, *Developer: Reload Window*. |
| Windows: `Filename too long` (git), `WinError 3` under `.snakemake/` | 260-character path limit | Clone near the drive root (`C:\ws\niwrap-workshop`); `git config --global core.longpaths true`. |
| Pulls fail with TLS or proxy errors | Corporate network | Dry mode. |
| `work/` keeps growing | Each call gets a new folder | Delete `work/` any time. |

## Without Docker: DryRunner

For anyone whose smoke test stopped at Docker, or whose Docker breaks mid-session. Decide by minute 10; don't spend helper time installing Docker.

1. In the first code cell of each notebook, change `RUNNER = "auto"` to `RUNNER = "dry"`.
2. Calls still build and validate their commands, outputs are still named and chain, and the whole 03 pipeline runs. Bad types and out-of-range values still raise `StyxValidationError`.
3. No files are created: plot cells print `(dry run ...)`, Step 4 shows where files would go, input files aren't checked.
4. To see a call's command: `import shlex`, then `print(shlex.join(runner.last_cargs))` after the call. In 03, call the step functions one at a time.
5. Pair them with a neighbour who has Docker, and keep your pre-computed `derivatives/` on the projector during the hands-on.
6. `uv run snakemake -s snakemake/Snakefile --cores 1 -n` works without Docker.

`niwrap.use_graph()` over a `DryRunner` draws wrong edges (every dry output shares the root `.`). Over a real runner it's correct.

## Snakemake demo

```bash
uv run snakemake -s snakemake/Snakefile --cores 1 -n    # 3 preprocess + 3 registration jobs
uv run snakemake -s snakemake/Snakefile --cores 3       # outputs in derivatives/snakemake/
rm derivatives/snakemake/registration/sub-02_*          # re-run: only sub-02's registration runs
```

`snakemake/` comes from [niwrap-workflow-examples](https://github.com/styx-api/niwrap-workflow-examples) @ `869f772` (`examples/snakemake-niwrap/src/snakemake_niwrap`) with two changes: `config.yaml` points at this repo's `data/` and three subjects, and the scripts no longer `from snakemake.iocontainers import snakemake`. That import doesn't exist in Snakemake 9.27.0 (the version upstream's lockfile pins), so the upstream scripts crash with `ImportError`. Snakemake injects `snakemake` into scripts itself.

The scripts call `niwrap.use_auto()` without `data_dir`, so intermediates collect in `./styx_tmp/` (gitignored). Delete it after the demo.

## RBC demo

```bash
uvx --from git+https://github.com/childmindresearch/rbc@9eaf3ac rbc anatomical --help
uvx --from git+https://github.com/childmindresearch/rbc@9eaf3ac rbc anatomical data/ds000001 \
    -o derivatives/rbc --participant-label 01 --ants-threads 4
```

- RBC pins `niwrap>=0.9.3,<1.0` (resolves to 0.9.6), so it runs through `uvx` in its own environment. The first `uvx` call clones the repo with its atlases (~3 min); do it beforehand.
- Besides the workshop's two images, `rbc anatomical` runs AFNI (`3drefit`, `3dresample`): `docker pull --platform linux/amd64 afni/afni_make_build:AFNI_24.2.06` (0.8 GB).
- `--runner auto` (default) checks Docker, Podman, Apptainer/Singularity, then local, the same order as `niwrap.use_auto()`.
- Show `src/rbc/core/anatomical/segmentation.py` and `src/rbc/core/niwrap.py`. In niwrap 0.9 the nested-argument helpers lack the `_params` suffix (`ants.ants_apply_transforms_transform_file_name(...)`).

## Styx book vs. installed NiWrap 1.1.0

Attendees reading the book will hit these. Each was checked against the installed packages.

| Book | NiWrap 1.1.0 | Book page |
|---|---|---|
| `fsl.bet(infile=..., outfile=..., binary_mask=True)` | No `outfile` parameter. The output prefix is `maskfile` (default `img_bet`); `bet.outfile` is the output attribute. | Getting started |
| `fslreorient2std`, `robustfov`, `fast` without output names, outputs then passed on | Unnamed outputs are `None` and the next call fails validation. Pass `output_image=` / `out_basename=`. | anat_preproc |
| `fsl.bet(..., robust_iters=True)` | Valid call, but `-R` fails in `brainlife/fsl:6.0.4-patched2` (`dc: command not found`). | anat_preproc |
| `from niwrap import DockerRunner, GraphRunner` | Not exported. `niwrap` re-exports styxkit: `use_docker`, `use_auto`, `use_dry`, `use_graph`, `resolve_runner`, `DryRunner`, `LocalRunner`, ... Or `from styxdocker import DockerRunner`. | anat_preproc, mermaid |
| `get_global_runner().mermaid()`, `graph_runner.node_graph_mermaid()` | Neither exists; it's `generate_mermaid()`. | Runners, mermaid |
| Dynamic runners: hand-written `if`/`elif` over `DockerRunner`, `SingularityRunner`, `LocalRunner` | `niwrap.use_auto()` does the detection; `niwrap.resolve_runner()` reports the choice. | Dynamic runners |
| `DockerRunner(data_dir=...)` vs. `runner.data_dir = ...` | Both work. All runners, and `use_*()`, accept `data_dir` and `environ`. | Runners |
| Default output folder `styx_temp/` | `styx_tmp/` | I/O |
