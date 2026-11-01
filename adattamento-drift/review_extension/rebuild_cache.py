"""Rebuild immutable inference caches from the supplied fitted initial states."""
import argparse
import hashlib
import json
from pathlib import Path
import pickle
import shutil
import numpy as np
import experiment as e


def rebuild(data,models,cache,provenance):
    with np.load(data/'D.npz') as f:
        arrays={k:f[k] for k in f.files}
    expected=json.loads((provenance/'D.json').read_text())['array_sha256']
    for key,value in arrays.items():
        digest=hashlib.sha256(np.ascontiguousarray(value).tobytes()).hexdigest()
        if digest!=expected[key]:raise ValueError('D array mismatch: '+key)
    X=arrays['X']
    for folder in sorted(models.iterdir()):
        if not (folder/'model.pkl').is_file():continue
        destination=cache/folder.name;destination.mkdir(parents=True,exist_ok=True)
        # Only load the trusted fitted states supplied with this versioned package.
        with (folder/'model.pkl').open('rb') as f:state=pickle.load(f)
        model,transform=state['model'],state['transform']
        if folder.name.startswith('arf_'):
            score=e.predict_river(model,transform(X))
        else:
            R=np.lib.format.open_memmap(destination/'representation.npy',mode='w+',
                                       dtype=np.float64,shape=(len(X),8))
            for a in range(0,len(X),200000):
                R[a:a+200000]=model.rappresentazione(transform(X[a:a+200000]))
            R.flush();p=model.parametri();score=R@p[:-1]+p[-1];del R
        np.save(destination/'frozen_score.npy',score)
        shutil.copy2(folder/'model.pkl',destination/'model.pkl')
        shutil.copy2(folder/'ready.json',destination/'ready.json')
        print('restored',destination,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data',type=Path,required=True)
    p.add_argument('--models',type=Path,required=True);p.add_argument('--cache',type=Path,required=True)
    p.add_argument('--provenance',type=Path,required=True);a=p.parse_args()
    rebuild(a.data,a.models,a.cache,a.provenance)
