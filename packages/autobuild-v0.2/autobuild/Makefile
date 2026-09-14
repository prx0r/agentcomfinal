.PHONY: test demo

test:
	python -m pytest -q

demo:
	python -m autobuild.cli compile examples/breadup_minimum_moat/plan.json --out build/breadup
	python -m autobuild.cli prebuild build/breadup/target_spec.json --out build/breadup/prebuild_request.json
	python -m autobuild.cli apply-prebuild build/breadup/target_spec.json fixtures/prebuild_response.json --out build/breadup/target_spec.prebuilt.json
	python -m autobuild.cli bridges build/breadup/target_spec.prebuilt.json --out build/breadup/bridges
	python -m autobuild.cli accrue fixtures/run_contribution.json --ledger build/accretion.jsonl
