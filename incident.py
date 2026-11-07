"""Deterministic incident workflow and guarded fixture repair; stdlib only."""
import argparse, hashlib, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent
STATE = ROOT / '.incident-state.json'
TARGET = ROOT / 'checkout.py'
OLD = 'if coupon.upper() == "SAVE10":'
NEW = 'if (coupon or "").upper() == "SAVE10":'

def digest(b): return hashlib.sha256(b).hexdigest()
def emit(state, role, message):
    state['events'].append({'at': datetime.now(timezone.utc).isoformat(), 'role': role, 'message': message})
def save(s): STATE.write_text(json.dumps(s, indent=2), encoding='utf-8')
def read():
    if not STATE.exists(): raise ValueError('Run triage first.')
    return json.loads(STATE.read_text(encoding='utf-8'))
def triage():
    source = TARGET.read_bytes(); text = source.decode('utf-8'); logs = (ROOT/'logs/incident.log').read_text(encoding='utf-8')
    if text.count(OLD) != 1 or 'NoneType' not in logs: raise ValueError('Expected demo signature missing; refusing to propose a fix.')
    patch = text.replace(OLD, NEW, 1).encode('utf-8')
    s = {'status':'awaiting_approval','source_sha256':digest(source),'patch_sha256':digest(patch),'events':[]}
    emit(s,'triage','Checkout returns 500 for requests with no coupon; sample logs show 2 failures.')
    emit(s,'investigator',"Evidence: NoneType.upper in logs; checkout.total calls coupon.upper without checking for None.")
    emit(s,'fixer','Proposed one-line fix: treat a missing coupon as an empty string. No files changed.')
    emit(s,'gate','Human must review the proposed source and approve its SHA-256 before applying.')
    save(s); print('Awaiting approval. Proposed file SHA-256:',s['patch_sha256']); print('Change:', OLD, '->', NEW)
def approve(hash_value):
    s=read()
    if s['status'] != 'awaiting_approval': raise ValueError('No pending proposal.')
    original=TARGET.read_bytes()
    if digest(original)!=s['source_sha256']: raise ValueError('Source changed; run triage again.')
    patched=original.decode('utf-8').replace(OLD,NEW,1).encode('utf-8')
    if digest(patched)!=s['patch_sha256'] or hash_value!=s['patch_sha256']: raise ValueError('Approval hash does not match proposed fix.')
    TARGET.write_bytes(patched); s['status']='applied'; emit(s,'human','Approved exact proposed file hash '+hash_value); save(s)
    result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,text=True,capture_output=True)
    s['status']='verified' if result.returncode==0 else 'verification_failed'
    emit(s,'verifier',('PASS' if result.returncode==0 else 'FAIL')+' — regression suite (exit '+str(result.returncode)+')\n'+result.stdout+result.stderr)
    save(s); print(result.stdout+result.stderr); print('Status:',s['status']); return result.returncode
def main():
    parser=argparse.ArgumentParser(); sub=parser.add_subparsers(dest='cmd',required=True)
    sub.add_parser('triage'); sub.add_parser('status'); a=sub.add_parser('approve'); a.add_argument('sha256')
    args=parser.parse_args()
    try:
        if args.cmd=='triage': triage()
        elif args.cmd=='approve': return approve(args.sha256)
        else: print(json.dumps(read(),indent=2))
    except (ValueError, OSError) as e: print('Error:',e,file=sys.stderr); return 1
    return 0
if __name__=='__main__': sys.exit(main())
