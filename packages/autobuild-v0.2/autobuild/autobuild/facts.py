"""Typed append-only knowledge records."""
from .canonical import content_id,digest

def fact(subject,predicate,value,evidence_ids=None,qualifiers=None):
    semantic={'subject':subject,'predicate':predicate,'value':value,'qualifiers':qualifiers or {}}
    return {'kind':'FACT','id':content_id('fact',semantic),'subject':subject,'predicate':predicate,'value':value,'qualifiers':qualifiers or {},'evidence_ids':sorted(evidence_ids or []),'semantic_root':digest(semantic)}

def negative_fact(subject,predicate,reason,evidence_ids=None,qualifiers=None):
    semantic={'subject':subject,'predicate':predicate,'result':'FALSE','reason':reason,'qualifiers':qualifiers or {}}
    return {'kind':'NEGATIVE_FACT','id':content_id('negative',semantic),'subject':subject,'predicate':predicate,'result':'FALSE','reason':reason,'qualifiers':qualifiers or {},'evidence_ids':sorted(evidence_ids or []),'semantic_root':digest(semantic)}

def supersede(old_id,new_id,reason,evidence_ids=None):
    body={'old':old_id,'new':new_id,'reason':reason,'evidence_ids':sorted(evidence_ids or [])}
    return {'kind':'SUPERSEDE','id':content_id('supersede',body),**body}
