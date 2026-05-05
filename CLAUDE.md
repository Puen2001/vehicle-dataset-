# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Labels-only GitHub repo for the 11-class vehicle detection dataset. Images are stored on the SSD (`/Volumes/Puen_SSD/vehicle_dataset/`) and the office PC — never in this repo.

Companion app repo: `vehicle-counting-app` (inference, tracking, counting).

## Structure

```
labels/<class>/         YOLO .txt files — one per image, same stem as the image filename
configs/
  coco_drr7.names       class names in order (0–10)
  pipeline_config.yaml  GDINO + SAM2 settings for Label Studio backend
scripts/
  push_labels.py        sync SSD labels → this repo → git push (main daily tool)
  merge_dataset.py      build train/val split from SSD labeled/ folders
  rename_dataset.py     normalise filenames to <class>_####.jpg (run before push)
  export_dataset.py     build real-file copy for transfer to office PC
data.yaml               YOLO training config — path:. so it works on any machine
```

## 11 classes (IDs 0–10)

`person · car · bike · truck · bus · taxi · pickup · trailer · tuktuk · agri_truck · van`

`agri_truck` is in SKIP_CLASSES in the inference app — counted in labels but not displayed live.

## Daily label push

```bash
python scripts/push_labels.py --ssd /Volumes/Puen_SSD/vehicle_dataset
```

This is the only command needed after a labeling session. It copies, commits, and pushes in one step.

## Rules

- Never commit *.jpg / *.png — .gitignore enforces this.
- Never modify labels/ files directly in this repo — always edit via Label Studio then push_labels.py.
- data.yaml uses `path: .` — do not change to an absolute path.
- When adding a new class: update CLASS_NAMES in all four scripts, add a labels/<newclass>/ folder with .gitkeep, update data.yaml nc and names, update configs/coco_drr7.names.
