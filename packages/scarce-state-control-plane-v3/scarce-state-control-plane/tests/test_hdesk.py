import unittest,tempfile,json
from pathlib import Path
from unittest.mock import patch
import runtime.hdesk as h
class T(unittest.TestCase):
 def test_invalid_debug_kind_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'h.json'; p.write_text(json.dumps({'version':'3','tasks':[],'answers':[]}))
   with patch.object(h,'PATH',p):
    with self.assertRaises(ValueError): h.add('debugging','fix this')
 def test_bounded_answer(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'h.json'; p.write_text(json.dumps({'version':'3','tasks':[],'answers':[]}))
   with patch.object(h,'PATH',p):
    t=h.add('strategic_direction','pick',['x'] if False else None,['a','b'],'a','portfolio tradeoff',8,2)
    self.assertEqual(h.queue()['count'],1)
    with self.assertRaises(ValueError): h.answer(t['id'],'c')
    self.assertEqual(h.answer(t['id'],'a')['decision'],'a'); self.assertEqual(h.queue()['count'],0)
if __name__=='__main__': unittest.main()
