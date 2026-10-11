import subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class MentorOffline(unittest.TestCase):
 def test_node_synthetic_contract_and_frozen_identity(self):
  subprocess.run(['node','--test','tests/mentor_demo_contract.mjs'],cwd=ROOT,check=True,capture_output=True,text=True)
 def test_standalone_generation_and_syntax(self):
  subprocess.run(['node','scripts/build_mentor_demo.mjs','--check'],cwd=ROOT,check=True,capture_output=True,text=True)
  for p in ('tools/mentor-demo/identity.mjs','tools/mentor-demo/model.mjs','tools/mentor-demo/ui.mjs','scripts/build_mentor_demo.mjs'):
   subprocess.run(['node','--check',p],cwd=ROOT,check=True,capture_output=True,text=True)
if __name__=='__main__':unittest.main(verbosity=2)
