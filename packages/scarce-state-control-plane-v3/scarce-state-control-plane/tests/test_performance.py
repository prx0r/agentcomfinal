import unittest,tempfile
from pathlib import Path
from unittest.mock import patch
import runtime.performance as p
class T(unittest.TestCase):
 def test_simulation_does_not_promote(self):
  fake=[{'strategy_family':'photo_to_money','evidence_source':'simulation','result':'SUCCESS'} for _ in range(10)]
  with patch.object(p,'runs',lambda:fake):
   row=next(x for x in p.strategy_performance() if x['id']=='photo_to_money')
   self.assertEqual(row['real_attempts'],0); self.assertEqual(row['promotion_state'],'INSUFFICIENT_REAL_OUTCOMES'); self.assertEqual(row['simulation_attempts'],10)
 def test_real_outcomes_count(self):
  fake=[{'strategy_family':'photo_to_money','evidence_source':'economic','result':'SUCCESS'} for _ in range(3)]
  with patch.object(p,'runs',lambda:fake):
   row=next(x for x in p.strategy_performance() if x['id']=='photo_to_money')
   self.assertEqual(row['real_attempts'],3); self.assertEqual(row['promotion_state'],'PROMOTE_CANDIDATE'); self.assertGreater(row['scheduler_multiplier'],1)

 def test_real_record_requires_receipt(self):
  with tempfile.TemporaryDirectory() as d, patch.object(p,'PATH',Path(d)/'runs.jsonl'):
   with self.assertRaises(ValueError): p.record('breadup','marketplace_sale','economic','SUCCESS')
   r=p.record('breadup','marketplace_sale','economic','SUCCESS',receipt_ref='receipt:1')
   self.assertEqual(r['strategy_family'],'photo_to_money')

if __name__=='__main__': unittest.main()
