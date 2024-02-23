.PHONY: all target

# Target 'all' will run the 'run_commands' target
all: target

# Target to run commands from the JSON file
target:
	@jq -r '.[] | .commd' commd_selfplay_casino.json | while IFS= read -r cmmd; do \
		$$cmmd; \
	done