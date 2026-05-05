"""
Sync labels from SSD → this repo → git commit + push.

Run after every Label Studio export session:
    python scripts/push_labels.py --ssd /Volumes/Puen_SSD/vehicle_dataset
    python scripts/push_labels.py --ssd D:\\vehicle_dataset        (Windows)
"""

import argparse
import shutil
import subprocess
from collections import Counter
from pathlib import Path

CLASSES  = ['person','car','bike','truck','bus','taxi','pickup','trailer','tuktuk','agri_truck','van']
REPO_ROOT = Path(__file__).parent.parent


def parse_args():
    p = argparse.ArgumentParser(description="Sync SSD labels → repo → git push")
    p.add_argument('--ssd', required=True, help='Path to vehicle_dataset/ root on SSD')
    p.add_argument('--no-push', action='store_true', help='Commit but do not push')
    return p.parse_args()


def run(cmd: list, cwd: Path) -> str:
    result = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] {' '.join(cmd)}\n{result.stderr.strip()}")
    return result.stdout.strip()


def main():
    args    = parse_args()
    ssd     = Path(args.ssd)
    labeled = ssd / 'labeled'

    if not labeled.exists():
        print(f'[ERROR] SSD not found: {labeled}')
        print('        Connect the SSD and try again.')
        return

    print(f'\n{"="*50}')
    print(f'  PUSH LABELS')
    print(f'{"="*50}')

    added   = Counter()
    updated = Counter()

    for cls in CLASSES:
        src_dir = labeled / cls / 'labels'
        dst_dir = REPO_ROOT / 'labels' / cls
        dst_dir.mkdir(parents=True, exist_ok=True)

        if not src_dir.exists():
            continue

        for txt in src_dir.glob('*.txt'):
            dst = dst_dir / txt.name
            if not dst.exists():
                shutil.copy2(str(txt), str(dst))
                added[cls] += 1
            elif txt.read_bytes() != dst.read_bytes():
                shutil.copy2(str(txt), str(dst))
                updated[cls] += 1

    total_added   = sum(added.values())
    total_updated = sum(updated.values())

    print(f'\nSynced from SSD:')
    for cls in CLASSES:
        a = added[cls]
        u = updated[cls]
        if a or u:
            print(f'  {cls:12}: +{a} new  ~{u} updated')

    if total_added == 0 and total_updated == 0:
        print('  No changes — labels already up to date.')
        print(f'{"="*50}\n')
        return

    # Git commit
    run(['git', 'add', 'labels/'], cwd=REPO_ROOT)

    parts = []
    if total_added:   parts.append(f'+{total_added} new')
    if total_updated: parts.append(f'~{total_updated} updated')
    classes_changed = [c for c in CLASSES if added[c] or updated[c]]
    msg = f'labels: {", ".join(parts)} ({", ".join(classes_changed)})'

    run(['git', 'commit', '-m', msg], cwd=REPO_ROOT)
    print(f'\nCommit: "{msg}"')

    if not args.no_push:
        print('Pushing to GitHub...')
        out = run(['git', 'push'], cwd=REPO_ROOT)
        if out:
            print(f'  {out}')
        print('Done.')
    else:
        print('Skipped push (--no-push).')

    print(f'{"="*50}\n')


if __name__ == '__main__':
    main()
