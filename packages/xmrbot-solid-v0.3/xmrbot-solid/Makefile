.PHONY: run test validate mcp local clean
run:
	PYTHONPATH=src uvicorn xmrbot.app:app --host 127.0.0.1 --port 8000 --reload

test:
	PYTHONPATH=src pytest

validate:
	bash scripts/validate.sh

mcp:
	PYTHONPATH=src python -m xmrbot.mcp.stdio

local:
	PYTHONPATH=src python -m xmrbot.local.daemon serve

clean:
	rm -f xmrbot.db
