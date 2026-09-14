
import unittest
from runtime.graph import assert_acyclic,ready
from runtime.model import project
class T(unittest.TestCase):
 def test_acyclic(self): self.assertTrue(assert_acyclic())
 def test_ready(self):
  p=project('breadup'); r=ready(p,[]); self.assertEqual(len(r),1); self.assertEqual(r[0]['ordinal'],1)
  r2=ready(p,[p['checkpoints'][0]['id']]); self.assertEqual(r2[0]['ordinal'],2)
if __name__=='__main__': unittest.main()
