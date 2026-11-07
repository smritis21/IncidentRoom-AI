import unittest, tempfile, shutil, subprocess, sys, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class WorkflowTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.p=Path(self.tmp.name)
  for f in ('incident.py','checkout.py'): shutil.copy(ROOT/f,self.p/f)
  shutil.copytree(ROOT/'logs',self.p/'logs'); shutil.copytree(ROOT/'tests',self.p/'tests')
  # Restore the intentionally broken fixture if the caller is verifying a repair.
  p=self.p/'checkout.py'; p.write_text(p.read_text().replace('if (coupon or "").upper() == "SAVE10":','if coupon.upper() == "SAVE10":'))
 def tearDown(self): self.tmp.cleanup()
 def run_cli(self,*args): return subprocess.run([sys.executable,'incident.py',*args],cwd=self.p,capture_output=True,text=True)
 def test_gate_and_verification(self):
  self.assertEqual(self.run_cli('triage').returncode,0)
  s=json.loads((self.p/'.incident-state.json').read_text())
  self.assertNotEqual(self.run_cli('approve','wrong').returncode,0)
  self.assertIn('if coupon.upper()', (self.p/'checkout.py').read_text())
  # Avoid recursively running this workflow test from the child verification.
  (self.p/'tests'/'test_workflow.py').unlink()
  self.assertEqual(self.run_cli('approve',s['patch_sha256']).returncode,0)
  self.assertEqual(json.loads((self.p/'.incident-state.json').read_text())['status'],'verified')
 def test_changed_source_rejected(self):
  self.run_cli('triage'); s=json.loads((self.p/'.incident-state.json').read_text())
  with (self.p/'checkout.py').open('a') as f: f.write('\n# changed\n')
  self.assertNotEqual(self.run_cli('approve',s['patch_sha256']).returncode,0)
