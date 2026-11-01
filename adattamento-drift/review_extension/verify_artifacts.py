"""Check shipped artifact hashes without loading pickle models or raw data."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/'ARTIFACT_MANIFEST.json').read_text())
for name,expected in manifest['sha256'].items():
    path=root/name
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected:raise SystemExit('HASH MISMATCH: '+name)
validation=json.loads((root/'analysis/validation.json').read_text())
assert validation['complete'] and validation['runs']==55
review2=json.loads((root/'review2/analysis/validation.json').read_text())
assert review2['complete'] and review2['runs']==120 and review2['exact_repeat_trajectories']==30
review3=json.loads((root/'review3/analysis/validation.json').read_text())
assert review3['complete'] and review3['runs']==10 and review3['all_shared_trajectories_exact']
print(f"Verified {len(manifest['sha256'])} file hashes; 55 first-extension, 120 second-review and 10 matched-memory cells present.")
