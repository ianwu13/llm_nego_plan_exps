.PHONY: all casino dnd

# Target 'all' will run the 'run_commands' target
all: casino dnd

# Target to run commands from the JSON file
casino:
	@jq -r '.[] | .commd' commd_selfplay_casino.json | while IFS= read -r cmmd; do \
		$$cmmd; \
	done

dnd:
	@jq -r '.[] | .commd' commd_selfplay_dnd.json | while IFS= read -r cmmd; do \
		$$cmmd; \
	done