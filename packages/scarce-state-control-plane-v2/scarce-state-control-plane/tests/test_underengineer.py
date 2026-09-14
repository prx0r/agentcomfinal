import unittest
from runtime.underengineer import plan,ranked,feature_allowed,order
class T(unittest.TestCase):
 def test_minimal_path(self):
  p=plan('pogtown'); self.assertIn('game',p['minimal_live_product'].lower()); self.assertLessEqual(len(p['not_now']),10); self.assertIsNotNone(p['next_step'])
 def test_asset_campaigns_first_bucket(self):
  r=ranked(); self.assertTrue(r['asset_campaigns']); self.assertTrue(all(x['strategic_role']=='asset_campaign' for x in r['asset_campaigns']))
 def test_asset_campaign_first_event_is_asset_event(self):
  from runtime.model import projects
  for p in projects():
   if p['strategic_role']=='asset_campaign':
    events={a['acquisition_event'] for a in p['scarce_assets']}
    self.assertIn(p['underengineer']['first_real_moat_event'],events)
 def test_order_pulls_only_explicit_infra(self):
  o=order('breadup'); self.assertEqual(o['project_id'],'breadup'); self.assertIn('qp',o['required_components_now']); self.assertNotIn('plugin',o['required_components_now'])
 def test_feature_default_not_now(self):
  self.assertEqual(feature_allowed('pogtown','would_be_cool')['decision'],'NOT_NOW')
  self.assertEqual(feature_allowed('pogtown','verification')['decision'],'NOW')
if __name__=='__main__': unittest.main()
