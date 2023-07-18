"""
Few-shot prompt examples to be used in generating annotations
"""

# DND Prompt examples:
dnd_fs_texts = [
    'CONTEXT: "2 books 2 hats 2 balls" UTTERANCE: "hello"',
    'CONTEXT: "2 books 2 hats 1 balls" UTTERANCE: "what would you like?"',
    'CONTEXT: "1 books 4 hats 1 balls" UTTERANCE: "i would like 4 hats and you can have the rest"',
    'CONTEXT: "1 books 2 hats 3 balls" UTTERANCE: "ill take the balls and one book"',
    'CONTEXT: "2 books 2 hats 1 balls" UTTERANCE: "how about i take the ball and 1 book and 1 hat"',
    'CONTEXT: "1 books 2 hats 2 balls" UTTERANCE: "that will not work for me"',
    'CONTEXT: "4 books 2 hats 1 balls" UTTERANCE: "no deal. i want the ball and at least 2 books"',
    'CONTEXT: "1 books 1 hats 4 balls" UTTERANCE: "no i need 2 of the balls"',
    'CONTEXT: "1 books 3 hats 2 balls" UTTERANCE: "well that works perfect for me"',
    'CONTEXT: "3 books 2 hats 1 balls" UTTERANCE: "deal you get all books i get the rest"'
    ]
dnd_fs_texts_w_dh = [
    'CONTEXT: "2 books 2 hats 2 balls" DIALOGUE_HISTORY: "" UTTERANCE: "hello"',
    'CONTEXT: "2 books 2 hats 1 balls" DIALOGUE_HISTORY: "" UTTERANCE: "what would you like?"',
    'CONTEXT: "1 books 4 hats 1 balls" DIALOGUE_HISTORY: "" UTTERANCE: "i would like 4 hats and you can have the rest"',
    'CONTEXT: "1 books 2 hats 3 balls" DIALOGUE_HISTORY: "" UTTERANCE: "ill take the balls and one book"',
    'CONTEXT: "2 books 2 hats 1 balls" DIALOGUE_HISTORY: "THEM: ill take the hats and the ball. YOU: i can not make that deal . if we can split the hats and i can take the books you can have the ball" UTTERANCE: "how about i take the ball and 1 book and 1 hat"',
    'CONTEXT: "1 books 2 hats 2 balls" DIALOGUE_HISTORY: "THEM: i only need the book . <eos> YOU: i only need the book? THEM: i need the book. you can have the hats and the balls." UTTERANCE: "that will not work for me"',
    'CONTEXT: "4 books 2 hats 1 balls" DIALOGUE_HISTORY: "THEM: i would like the ball and the books please YOU: give me the ball and hats and you could keep the books" UTTERANCE: "no deal . i want the ball and at least 2 books"',
    'CONTEXT: "1 books 1 hats 4 balls" DIALOGUE_HISTORY: "THEM: i need the book and the hat you can have the balls YOU: i need the hat and 2 of the balls. you can have the book and 2 of the balls. THEM: i need the book and 3 balls" UTTERANCE: "no, i need 2 of the balls"',
    'CONTEXT: "1 books 3 hats 2 balls" DIALOGUE_HISTORY: "THEM: i need the hats and the book" UTTERANCE: "well that works perfect for me"',
    'CONTEXT: "3 books 2 hats 1 balls" DIALOGUE_HISTORY: "YOU: i need the ball and 1 hat. THEM: you can everything but books. thats all i need." UTTERANCE: "deal you get all books i get the rest"'
]

dnd_fs_annots = [
    'Greet',
    'Inquire',
    'Propose books=0 hats=4 balls=0',
    'Propose books=1 hats=0 balls=3',
    'Propose books=1 hats= 1 balls=1',
    'Disagree',
    'Disagree',
    'Insist',
    'Agree',
    'Agree',
]
dnd_fs_annots_no_vc = [
    'Greet',
    'Inquire',
    'Propose',
    'Propose',
    'Propose',
    'Disagree',
    'Disagree',
    'Insist',
    'Agree',
    'Agree',
]

# CaSiNo Prompt examples:
casino_fs_texts = [
    'Hello, how are you today?',
    'Oh I wouldnt want for you to freeze',
    'Lets try to make a deal that benefits us both!',
    'We have plenty of water to space',
    'What supplies do you prefer to take the most of?',
    'Do you have help carrying all that extra firewood? Could be heavy?',
    'That would leave me with no water',
    'I cant take cold and would badly need to have more firewood',
    'We got kids on this trip, they need food too.',
    'Hello, I need supplies for the trip!'
]
casino_fs_texts_w_dh = []

casino_fs_annots_l1 = [
    'Prosocial Generic',
    'Prosocial Generic',
    'Prosocial Generic',
    'Prosocial About Preferences',
    'Prosocial About Preferences',
    'Proself Generic',
    'Proself Generic',
    'Proself About Preferences',
    'Proself About Preferences',
    'Non-strategic'
]
casino_fs_annots_l2_selref = [
    'Small Talk',
    'Empathy/Coordination',
    'Empathy/Coordination',
    'No-need',
    'Elicit Preferences',
    'Undervalue Partner',
    'Vouch Fairness',
    'Self/Other Need',
    'Self/Other Need',
    'Non-strategic'
]