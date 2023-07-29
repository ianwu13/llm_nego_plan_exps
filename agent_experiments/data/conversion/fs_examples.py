"""
Few-shot prompt examples to be used in generating annotations
"""

from collections import OrderedDict

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

# FINAL FS EXAMPLES

# DND RB Format
dnd_fs_examples = [
    'CONTEXT: "2 books 2 hats 2 balls" UTTERANCE: "hello"',
    'CONTEXT: "2 books 2 hats 1 balls" UTTERANCE: "what would you like?"',
    'CONTEXT: “1 books 1 hats 3 balls” UTTERANCE: “do you want the hat?”',
    'CONTEXT: "1 books 4 hats 1 balls" UTTERANCE: "i would like 4 hats and you can have the rest"',
    'CONTEXT: "1 books 2 hats 3 balls" UTTERANCE: "ill take the balls and one book"',
    'CONTEXT: "2 books 3 hats 1 balls" UTTERANCE: "i want all the books"',
    'CONTEXT: "1 books 2 hats 2 balls" UTTERANCE: "that will not work for me"',
    'CONTEXT: "1 books 1 hats 4 balls" UTTERANCE: "no, i need 2 of the balls"',
    'CONTEXT: "1 books 3 hats 2 balls" UTTERANCE: "well that works perfect for me"',
    'CONTEXT: "1 books 3 hats 2 balls" UTTERANCE: "<selection>"'
    ]

dnd_fs_examples_dh = [
    'CONTEXT: "2 books 2 hats 2 balls" DIALOGUE_HISTORY: "" UTTERANCE: "hello"',
    'CONTEXT: "2 books 2 hats 1 balls" DIALOGUE_HISTORY: "" UTTERANCE: "what would you like?"',
    'CONTEXT: “1 books 1 hats 3 balls” DIALOGUE_HISTORY: "YOU: i would like all 3 balls THEM: deal . i need 1 book" UTTERANCE: “do you want the hat?”',
    'CONTEXT: "1 books 4 hats 1 balls" DIALOGUE_HISTORY: "" UTTERANCE: "i would like 4 hats and you can have the rest"',
    'CONTEXT: "1 books 2 hats 3 balls" DIALOGUE_HISTORY: "" UTTERANCE: "ill take the balls and one book"',
    'CONTEXT: "2 books 3 hats 1 balls" DIALOGUE_HISTORY: "" UTTERANCE: "i want all the books"',
    'CONTEXT: "1 books 2 hats 2 balls" DIALOGUE_HISTORY: "THEM: i only need the book . <eos> YOU: i only need the book? THEM: i need the book. you can have the hats and the balls." UTTERANCE: "that will not work for me"',
    'CONTEXT: "1 books 1 hats 4 balls" DIALOGUE_HISTORY: "THEM: i need the book and the hat you can have the balls YOU: i need the hat and 2 of the balls. you can have the book and 2 of the balls. THEM: i need the book and 3 balls" UTTERANCE: "no, i need 2 of the balls"',
    'CONTEXT: "1 books 3 hats 2 balls" DIALOGUE_HISTORY: "THEM: i need the hats and the book" UTTERANCE: "well that works perfect for me"',
    'CONTEXT: "1 books 3 hats 2 balls" DIALOGUE_HISTORY: "" UTTERANCE: "<selection>"'
    ]

dnd_annots = [
    'Greet',
    'Inquire',
    'Inquire hats',
    'Propose books=0 hats=4 balls=0',
    'Propose books=1 hats=0 balls=3',
    'Propose books=2',
    'Disagree',
    'Insist',
    'Agree',
    'Agree'
    ]

# CaSiNo DND Format
casino_dnd_format_examples = [
    'CONTEXT: "high priority food, low priority water, medium priority firewood" UTTERANCE: "Hello. How are you?"',
    "CONTEXT: “medium food low water high firewood” UTTERANCE: “Hello! Let's work together on a deal for these packages, shall we? What are you most interested in?”", 'CONTEXT: "medium food low water high firewood" UTTERANCE: "Hello! Let\'s work together on a deal for these packages, shall we? What are you most interested in?"',
    'CONTEXT: "low priority food, high priority water, medium priority firewood" UTTERANCE: "What about the food? How much food do you need for camping?"',
    'CONTEXT: "high priority food, medium priority water, low priority firewood" UTTERANCE: "i will give you that in exchange for 1 food and 3 water with 2 firewood"',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" UTTERANCE: "I like to hike and will need additional water. Can I take one package and you can have the other two?"',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" UTTERANCE: "I dont think I am okay with that. Food is essential to our groups morale when camping. We would like 1 additional food preferably."',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" UTTERANCE: "No i really need all the water, if its a deal breaker than you can have all the firewood."',
    'CONTEXT: "high priority food, low priority water, medium priority firewood" UTTERANCE: "that sounds like a good deal to me"'
    ]

casino_dnd_format_examples_dh = [
    'CONTEXT: "high priority food, low priority water, medium priority firewood" DIALOGUE_HISTORY: "" UTTERANCE: "Hello. How are you?"',
    "CONTEXT: “medium food low water high firewood” DIALOGUE_HISTORY: “” UTTERANCE: “Hello! Let's work together on a deal for these packages, shall we? What are you most interested in?”", 'CONTEXT: "medium food low water high firewood" DIALOGUE_HISTORY: "" UTTERANCE: "Hello! Let\'s work together on a deal for these packages, shall we? What are you most interested in?"',
    'CONTEXT: "low priority food, high priority water, medium priority firewood" DIALOGUE_HISTORY: "THEM: I really need 3 firewood because I am always cold. YOU: If I gave you 3 firewood, would you give me 3 water? I can do without the wood, but the water is really important to stay hydrated. THEM: I can give you 2 water, but I have to have 1 to help me when I am cooking." UTTERANCE: "What about the food? How much food do you need for camping?"',
    'CONTEXT: "high priority food, medium priority water, low priority firewood" DIALOGUE_HISTORY: "THEM: In this extra package I need two food YOU: wow that is a much THEM: because of my big size I want two extra food package" UTTERANCE: "i will give you that in exchange for 1 food and 3 water with 2 firewood"',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" DIALOGUE_HISTORY: "YOU: medium priority food, high priority water, low priority firewood THEM: Hello!  I\'ve been super thirsty and as a result I was wondering if I could get all 3 packages of water?" UTTERANCE: "I like to hike and will need additional water. Can I take one package and you can have the other two?"',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" DIALOGUE_HISTORY: "THEM: Water is a little important to us too though , if possible maybe we can split that or maybe we can get some more food in replacement. YOU: That may be possible.... What did you have in mind for the food replacement?  THEM: You can have all the water if we can have all the food?" UTTERANCE: "I dont think I am okay with that. Food is essential to our groups morale when camping. We would like 1 additional food preferably."',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" DIALOGUE_HISTORY: "THEM: that will work for me - how about i take 2 food, and all the firewood - i am hoping to teach my boys campfire songs - they need other hobbies that dont include electronics :). You can have 1 food and all the water?  YOU: I would like just 1 firewood so we can have a smores night with the younger kids if that works? THEM: that works for me - would you be willing to give me 1 of the waters that way i at least have a little extra" UTTERANCE: "No i really need all the water, if its a deal breaker than you can have all the firewood."',
    'CONTEXT: "high priority food, low priority water, medium priority firewood" DIALOGUE_HISTORY: "THEM: I really need some food, but I could also use extra firewood. It is supposed to be pretty cold at night and we would love to cook up some smores. YOU: I hear you we have the same issues well you can have either 2 food or 2 firewood what would you prefer? THEM: I would prefer 2 food. I could give you 1 food, 2 firewood and 2 water?" UTTERANCE: "that sounds like a good deal to me"'
    ]

casino_dnd_format_annots = [
    'Greet',
    'Inquire',
    'Inquire',
    'Inquire food',
    'Propose food=0 water=1 firewood=3',
    'Propose water=2',
    'Disagree',
    'Insist',
    'Agree'
]

#CaSiNo Custom Format
casino_cust_format_examples = [
    'CONTEXT: "high priority food, low priority water, medium priority firewood" UTTERANCE: "I am good. I am pretty excited for the trip this weekend. what about you?"',
    'CONTEXT: "high priority food, low priority water, medium priority firewood" UTTERANCE: "Would you be willing to take more firewood for less food?"',
    'CONTEXT: "medium priority food, low priority water, high priority firewood" UTTERANCE: "I am willing to share everything."',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" UTTERANCE: "I am good at making fire and have a starter so I can give up all the wood."',
    'CONTEXT: "high priority food, low priority water, medium priority firewood" UTTERANCE: "Yes!  Would you mind sharing your highest priority item with me?  My most valued item right now is Food actually"',
    'CONTEXT: "low priority food, high priority water, medium priority firewood" UTTERANCE: "What about the food? How much food do you need for camping?"',
    'CONTEXT: "high priority food, low priority water, medium priority firewood" UTTERANCE: "Hi. Why do you need so many food packages?"',
    'CONTEXT: "low priority food, high priority water, medium priority firewood" UTTERANCE: "Do you have help carrying all that extra firewood? Could be heavy?"',
    'CONTEXT: "low priority food, high priority water, medium priority firewood" UTTERANCE: "Sure that sounds fair to me, we both get what we need."',
    'CONTEXT: "high priority food, medium priority water, low priority firewood" UTTERANCE: "ME as well! we are a group of big eaters, and are looking to take lots of food."',
    'CONTEXT: "low priority food, medium priority water, high priority firewood" UTTERANCE: "Hey, nice getting to interact with you. I would like to have additional packages of firewood and water"',
    'CONTEXT: "high priority food, medium priority water, low priority firewood" UTTERANCE: "i will give you that in exchange for 1 food and 3 water with 2 firewood"',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" UTTERANCE: "I like to hike and will need additional water. Can I take one package and you can have the other two?"',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" UTTERANCE: "I dont think I am okay with that. Food is essential to our groups morale when camping. We would like 1 additional food preferably."',
    'CONTEXT: "high priority food, low priority water, medium priority firewood" UTTERANCE: "that sounds like a good deal to me"'
    ]

casino_cust_format_examples_dh = [
    'CONTEXT: "high priority food, low priority water, medium priority firewood" DIALOGUE_HISTORY: "THEM: Hello. How are you?" UTTERANCE: "I am good. I am pretty excited for the trip this weekend. what about you?"',
    'CONTEXT: "high priority food, low priority water, medium priority firewood" DIALOGUE_HISTORY: "THEM: What are you most interested in getting? YOU: I think food is my highest priority, What about you? THEM: Food is also my highest priority, but firewood is also pretty close for me." UTTERANCE: "Would you be willing to take more firewood for less food?"',
    'CONTEXT: "medium priority food, low priority water, high priority firewood" DIALOGUE_HISTORY: "THEM: Hi, are you excited for the camping trip? YOU: Hello! I am very excited! How about you? THEM: Yes!  Would you mind sharing your highest priority item with me?  My most valued item right now is Food actually" UTTERANCE: "I am willing to share everything."',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" DIALOGUE_HISTORY: "THEM: I do need more food than firewood, If I could get 3 food and 2 firewood. You can get 3 water and 1 firewood. YOU: I do need some food. I would like to get at least 1 food. You can still get 3 firewood. THEM: I could use water as well, so I could get 1 water, 2 food and 2 firewood" UTTERANCE: "I am good at making fire and have a starter so I can give up all the wood."',
    'CONTEXT: "high priority food, low priority water, medium priority firewood" DIALOGUE_HISTORY: "THEM: medium priority food, low priority water, high priority firewood YOU: Hi, are you excited for the camping trip? THEM: Hello! I am very excited! How about you?" UTTERANCE: "Yes!  Would you mind sharing your highest priority item with me?  My most valued item right now is Food actually"',
    'CONTEXT: "low priority food, high priority water, medium priority firewood" DIALOGUE_HISTORY: "THEM: I really need 3 firewood because I am always cold. YOU: If I gave you 3 firewood, would you give me 3 water? I can do without the wood, but the water is really important to stay hydrated. THEM: I can give you 2 water, but I have to have 1 to help me when I am cooking." UTTERANCE: "What about the food? How much food do you need for camping?"',
    'CONTEXT: "high priority food, low priority water, medium priority firewood" DIALOGUE_HISTORY: "YOU: high priority food, low priority water, medium priority firewood THEM: Hi.  I am looking at possibly taking 3 of the food packages, 2 of the water packages and one of the firewood." UTTERANCE: "Hi. Why do you need so many food packages?"',
    'CONTEXT: "low priority food, high priority water, medium priority firewood" DIALOGUE_HISTORY: "THEM: Sure, I can spare that YOU: I really appreciate you being so kind. I have so much medication to take and have to make sure I take it with lots of water. THEM: Its ok" UTTERANCE: "Do you have help carrying all that extra firewood? Could be heavy?"',
    'CONTEXT: "low priority food, high priority water, medium priority firewood" DIALOGUE_HISTORY: "THEM: This offer is good for me but I need some water too. Can we share the water and have all the firewood? YOU: No, I offer you 3 food, and 1 water.  I would like 2 water and 3 firewood. THEM: Well this is perfect for me. I agree with 3 food and 1 water. Do you also agree?" UTTERANCE: "Sure that sounds fair to me, we both get what we need."',
    'CONTEXT: "high priority food, medium priority water, low priority firewood" DIALOGUE_HISTORY: "THEM: Hello, how are you doing today? YOU: i am doing great! how about you? THEM: I\'m doing pretty well, just preparing for this camping trip." UTTERANCE: "ME as well! we are a group of big eaters, and are looking to take lots of food."',
    'CONTEXT: "low priority food, medium priority water, high priority firewood" DIALOGUE_HISTORY: "YOU: low priority food, medium priority water, high priority firewood THEM: Hello, what are your preferences for food, water, and firewood?" UTTERANCE: "Hey, nice getting to interact with you. I would like to have additional packages of firewood and water"',
    'CONTEXT: "high priority food, medium priority water, low priority firewood" DIALOGUE_HISTORY: "THEM: In this extra package I need two food YOU: wow that is a much THEM: because of my big size I want two extra food package" UTTERANCE: "i will give you that in exchange for 1 food and 3 water with 2 firewood"',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" DIALOGUE_HISTORY: "YOU: medium priority food, high priority water, low priority firewood THEM: Hello!  I\'ve been super thirsty and as a result I was wondering if I could get all 3 packages of water?" UTTERANCE: "I like to hike and will need additional water. Can I take one package and you can have the other two?"',
    'CONTEXT: "medium priority food, high priority water, low priority firewood" DIALOGUE_HISTORY: "THEM: Water is a little important to us too though , if possible maybe we can split that or maybe we can get some more food in replacement. YOU: That may be possible.... What did you have in mind for the food replacement?  THEM: You can have all the water if we can have all the food?" UTTERANCE: "I dont think I am okay with that. Food is essential to our groups morale when camping. We would like 1 additional food preferably."',
    'CONTEXT: "high priority food, low priority water, medium priority firewood" DIALOGUE_HISTORY: "THEM: I really need some food, but I could also use extra firewood. It is supposed to be pretty cold at night and we would love to cook up some smores. YOU: I hear you we have the same issues well you can have either 2 food or 2 firewood what would you prefer? THEM: I would prefer 2 food. I could give you 1 food, 2 firewood and 2 water?" UTTERANCE: "that sounds like a good deal to me"'
    ]

casino_cust_format_annots = [
    'Small-talk',
    'Empathy/Coordination',
    'Empathy/Coordination',
    'No-need firewood',
    'Elicit Preference',
    'Elicit Preference food',
    'Undervalue food',
    'Undervalue firewood',
    'Vouch Fairness',
    'Express Preference food',
    'Express Preference water firewood',
    'Propose food=0 water=1 firewood=3',
    'Propose water=2',
    'Disagree',
    'Agree'
    ]

casino_cust_format_multilab_annots = [
    'Small-talk, Empathy/Coordination',
    'Empathy/Coordination',
    'Empathy/Coordination',
    'No-need firewood',
    'Elicit Preference,Express Preference food',
    'Elicit Preference food',
    'Elicit Preference food,Undervalue food',
    'Undervalue firewood',
    'Vouch Fairness,Agree',
    'Small-talk,Express Preference food',
    'Small-talk,Express Preference water firewood',
    'Propose food=0 water=1 firewood=3',
    'Small-talk,Propose water=2',
    'Disagree,Express Preference food',
    'Agree'
    ]

# FINAL E.G. EXAMPLES

dnd_rb_format = OrderedDict({
    '"Greet"': '"hello"', 
    '"Inquire"': {'"Inquire"': '"what would you like"', '"Inquire hats"': '"do you want the hat?"'},
    '"Propose"': {
        '"Propose books=0 hats=4 balls=0"': '"i would like 4 hats and you can have the rest"',
        '"Propose books=1 hats=0 balls=3"': '"ill take the balls and one book"',
        '"Propose books=2"': '"i want all the books"'
    },
    '"Insist"': '"no, i need 2 of the balls"', 
    '"Disagree"': '"that will not work for me"',
    '"Agree"': '"well that works perfect for me"'
})

casino_dnd_format = OrderedDict({
    '"Greet"': '"Hello. How are you?"', 
    '"Inquire"': {'"Inquire"': '"What are you most interested in?"', '"Inquire foor"': '"How much food do you need for camping?"'},
    '"Propose"': {
        '"Propose food=1 water=3 firewood=2"': '"i will give you that in exchange for 1 food and 3 water with 2 firewood"',
        '"Propose water=2"': '"I like to hike and will need additional water. Can I take one package and you can have the other two?"'    
    },
    '"Insist"': '"No i really need all the water, if its a deal breaker than you can have all the firewood."', 
    '"Disagree"': '"I dont think I am okay with that."', 
    '"Agree"': '"that sounds like a good deal to me" or "Submit-Deal"' 
})

casino_cust_format = OrderedDict({
    '"Small-talk"': '"I am good. I am pretty excited for the trip this weekend. what about you?"', 
    '"Empathy/Coordination"': '"I am willing to share everything."', 
    '"Elicit Preference"': {
        '"Elicit Preference"': '"Yes!  Would you mind sharing your highest priority item with me?"', 
        '"Elicit Preference food"': '"What about the food? How much food do you need for camping?"', 
    },
    '"Express Preference"': {
        '"Express Preference food"': '"Me as well! we are a group of big eaters, and are looking to take lots of food."', 
        '"Express Preference water firewood"': '"Hey, nice getting to interact with you. I would like to have additional packages of firewood and water"', 
    },
    '"Propose"': {
        '"Propose water=2"': '"I like to hike and will need additional water."', 
        '"Propose food=0 water=1 firewood=3"': '"i will give you that in exchange for 1 food and 3 water with 2 firewood"',
    },
    '"Vouch Fairness"': '"Sure that sounds fair to me, we both get what we need."', 
    '"Undervalue"': {
        '"Undervalue food"': '"Hi. Why do you need so many food packages?"', 
        '"Undervalue firewood"': '"Do you have help carrying all that extra firewood? Could be heavy"', 
    },
    '"No-need"': {
        '"No-need firewood"': '"I am good at making fire and have a starter so I can give up all the wood."'
    },
    '"Disagree"': '"I dont think I am okay with that."', 
    '"Agree"': '"that sounds like a good deal to me" or "Submit-Deal"' 
})
