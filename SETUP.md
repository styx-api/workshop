# Before the workshop

Do this at home or at work, not at the venue: the FSL image is a 7 GB download. Allow 30 minutes, mostly waiting.

## You need

| | |
|---|---|
| Disk | 35 GB free (the FSL image is 23.5 GB unpacked) |
| RAM | 8 GB, 16 GB recommended |
| Docker | [Docker Desktop](https://docs.docker.com/get-started/get-docker/) on macOS/Windows, Docker Engine on Linux |
| Editor | [VS Code](https://code.visualstudio.com/) with the Python and Jupyter extensions, or JupyterLab (installed below) |

You don't need FSL, ANTs or Python. uv installs Python; the tools run in containers.

In Docker Desktop, *Settings → Resources*: at least 4 CPUs and 8 GB memory.

Apple Silicon (M1–M4): the images are amd64 only. Turn on *Settings → General → Use Rosetta for x86_64/amd64 emulation*. It works, more slowly.

## 1. Install uv

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Open a new terminal and check `uv --version`.

## 2. Get the materials

```bash
git clone <workshop repository URL> niwrap-workshop
cd niwrap-workshop
uv sync
```

`uv sync` installs Python 3.13 if needed and the pinned packages into `.venv/`. Run all later commands from this folder.

## 3. Download the data (50 MB)

```bash
uv run scripts/fetch_data.py
```

Three T1w images from [OpenNeuro ds000001](https://openneuro.org/datasets/ds000001) go to `data/ds000001/`, the MNI152NLin2009cAsym template from [TemplateFlow](https://www.templateflow.org/) to `data/templateflow/`.

## 4. Pull the images (7 GB)

macOS, Linux, or Windows with Git Bash/WSL:

```bash
bash scripts/prepull_images.sh
```

Windows PowerShell:

```powershell
docker pull --platform linux/amd64 brainlife/fsl:6.0.4-patched2
docker pull --platform linux/amd64 antsx/ants:v2.5.3
```

An interrupted pull resumes when you run it again.

## 5. Smoke test

```bash
uv run scripts/smoke_test.py
```

Expect four `ok` lines and `All good.` in under a minute.

## 6. Open the notebooks

- VS Code: open the `niwrap-workshop` folder, then `notebooks/01_first_calls.ipynb`, and select the `.venv` kernel (top right).
- JupyterLab: `uv run jupyter lab notebooks/`

Run the first code cell of `01_first_calls.ipynb`. No error means you're ready.

## No Docker?

Come anyway. Do steps 1–3 and 5 (the smoke test will stop at the Docker check). In each notebook, change

```python
RUNNER = "auto"
```

to `RUNNER = "dry"`. Commands are then built and checked but not run, so you can write the whole pipeline, just without images to look at.

## Troubleshooting

| Problem | Fix |
|---|---|
| `uv: command not found` | Open a new terminal. |
| `FAIL docker is installed but not running` | Start Docker Desktop and wait for *Engine running*. |
| `no space left on device` while pulling | Free disk space, or move Docker's disk image (*Settings → Resources → Advanced*). |
| `no matching manifest for linux/arm64` | Use the `--platform linux/amd64` commands and enable Rosetta. |
| Windows: `Filename too long` during `git clone` | `git config --global core.longpaths true`, clone again. |
| VS Code doesn't list `.venv` | `uv sync`, then *Developer: Reload Window*. |

Still stuck? Email the organizers the output of `uv run scripts/smoke_test.py`.
