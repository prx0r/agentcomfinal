from .canonical import digest
from .delta import changeset

def transformation_receipt(before, after, transform_id, reasons=None, evidence_ids=None):
    cs=changeset(before,after,transform_id,reasons,evidence_ids)
    receipt={"kind":"TRANSFORMATION_RECEIPT","version":"1.0","transform_id":transform_id,"input_root":cs["before_root"],"output_root":cs["after_root"],"changes_root":cs["changes_root"],"reason_ids":sorted(reasons or []),"evidence_ids":sorted(evidence_ids or [])}
    receipt["receipt_id"]=digest(receipt)
    return {"changeset":cs,"receipt":receipt}
