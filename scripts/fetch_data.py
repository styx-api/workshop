"""Download the workshop dataset: a few T1w images from OpenNeuro ds000001 and the
MNI152NLin2009cAsym template from TemplateFlow.

    uv run scripts/fetch_data.py                 # sub-01..03 into ./data
    uv run scripts/fetch_data.py --subjects 01   # just one subject
"""

import argparse
import shutil
import urllib.request
from pathlib import Path

OPENNEURO = "https://s3.amazonaws.com/openneuro.org/ds000001"
TEMPLATEFLOW = "https://templateflow.s3.amazonaws.com"
TEMPLATE = "MNI152NLin2009cAsym"
TEMPLATE_FILES = [
    "template_description.json",
    "LICENSE",
    f"tpl-{TEMPLATE}_res-01_T1w.nii.gz",
    f"tpl-{TEMPLATE}_res-01_desc-brain_T1w.nii.gz",
    f"tpl-{TEMPLATE}_res-01_desc-brain_mask.nii.gz",
]


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  have {dest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    with urllib.request.urlopen(url, timeout=60) as response, tmp.open("wb") as f:
        shutil.copyfileobj(response, f)
    tmp.replace(dest)
    print(f"  got  {dest}")


def fetch_bids(out: Path, subjects: list[str]) -> None:
    bids = out / "ds000001"
    for name in ["dataset_description.json", "participants.tsv", "README"]:
        download(f"{OPENNEURO}/{name}", bids / name)
    for sub in subjects:
        rel = f"sub-{sub}/anat/sub-{sub}_T1w.nii.gz"
        download(f"{OPENNEURO}/{rel}", bids / rel)


def fetch_template(out: Path) -> None:
    tpl = out / "templateflow" / f"tpl-{TEMPLATE}"
    for name in TEMPLATE_FILES:
        download(f"{TEMPLATEFLOW}/tpl-{TEMPLATE}/{name}", tpl / name)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=Path("data"))
    parser.add_argument("--subjects", nargs="+", default=["01", "02", "03"])
    args = parser.parse_args()

    print(f"OpenNeuro ds000001 -> {args.out / 'ds000001'}")
    fetch_bids(args.out, args.subjects)
    print(f"TemplateFlow {TEMPLATE} -> {args.out / 'templateflow'}")
    fetch_template(args.out)


if __name__ == "__main__":
    main()
