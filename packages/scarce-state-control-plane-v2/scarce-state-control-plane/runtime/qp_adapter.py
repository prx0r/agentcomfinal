
PROOF_LEVELS={f'V{i}':i for i in range(13)}

def authority_required(checkpoint):
    return checkpoint.get('authority','M') in {'A','H'}

def grant_satisfies(checkpoint, grant):
    if checkpoint.get('authority')=='M': return True, 'machine-safe checkpoint'
    if checkpoint.get('authority')=='H': return False, 'human completion required'
    if not grant: return False, 'missing grant'
    need=PROOF_LEVELS.get(checkpoint.get('minimum_proof_level','V0'),0)
    got=PROOF_LEVELS.get(grant.get('proof_level','V0'),0)
    if got < need: return False, f'proof level {got} < {need}'
    if checkpoint['id'] not in grant.get('checkpoint_ids',[]): return False, 'grant not scoped to checkpoint'
    return True, 'grant accepted'
