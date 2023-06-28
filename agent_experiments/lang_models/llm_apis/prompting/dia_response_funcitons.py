"""
Functions which convert instances from datasethandler and corresponding annotatins from llms into string (line) outputs
for raw dataset files
"""


# TODO MAKE THIS WORK WHEN NEEDED
def example_response_func(inst):
    return [f"Respond to this: {chat_item['text']}" for chat_item in inst['chat_logs']]
