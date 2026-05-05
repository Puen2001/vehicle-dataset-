# vehicle-dataset

YOLO label repository for the vehicle detection system. **Images are not stored here** — labels, configs, and scripts only.

Used by [`vehicle-counting-app`](https://github.com/Puen2001/vehicle-counting-app).

---

## Classes

| ID | Name | ID | Name |
|---|---|---|---|
| 0 | person | 6 | pickup |
| 1 | car | 7 | trailer |
| 2 | bike | 8 | tuktuk |
| 3 | truck | 9 | agri_truck |
| 4 | bus | 10 | van |
| 5 | taxi | | |

---

## Structure

```
labels/<class>/     ← YOLO .txt label files (one per image, same stem as image filename)
configs/            ← class names, GDINO pipeline config
scripts/            ← dataset tools
data.yaml           ← YOLO training config (nc:11)
```

---

## Workflow

### Add new labels (after reviewing in Label Studio)

```bash
# Sync labels from SSD → repo → GitHub
python scripts/push_labels.py --ssd /Volumes/Puen_SSD/vehicle_dataset

# On Windows (office PC)
python scripts/push_labels.py --ssd D:\vehicle_dataset
```

### Build training dataset

```bash
# Merge all labeled data into train/val split
python scripts/merge_dataset.py --ssd /Volumes/Puen_SSD/vehicle_dataset

# Export transfer-ready copy (real files, no symlinks)
python scripts/export_dataset.py \
    --ssd /Volumes/Puen_SSD/vehicle_dataset \
    --out /Volumes/Puen_SSD/vehicle_dataset_export
```

### Rename files to safe ASCII format (before first push)

```bash
# Preview
python scripts/rename_dataset.py --ssd /Volumes/Puen_SSD/vehicle_dataset

# Apply
python scripts/rename_dataset.py --ssd /Volumes/Puen_SSD/vehicle_dataset --execute
```

---

## Office PC setup

```bash
git clone https://github.com/Puen2001/vehicle-dataset-.git
cd vehicle-dataset-

# Pull latest labels
git pull

# Build dataset (images must already be on the PC under storage/labeled/)
python scripts/merge_dataset.py --ssd /path/to/storage
```

---

## Rules

- Never commit image files — `.gitignore` blocks them automatically.
- `labels/` is append-only — do not delete existing `.txt` files without discussion.
- Always run `rename_dataset.py` before `push_labels.py` on new batches.
