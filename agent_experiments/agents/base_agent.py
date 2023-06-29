class Agent(object):
    """Agent's interface.

    The dialogue should proceed in the following way:

    1) feed_context to each of the agent.
    2) randomly pick an agent who will start the conversation.
    3) the starting agent will write down her utterance.
    4) the other agent will read the pronounced utterance.
    5) unless the end of dialogue is pronounced, swap the agents and repeat the steps 3-4.
    6) once the conversation is over, generate choices for each agent and calculate the reward.
    7) pass back to the reward to the update function.


    See Dialogue.run in the dialog.py for more details.
    """

    def feed_context(self, context):
        """Feed context in to start new conversation.

        context: a list of context tokens.
        """
        pass

    def read(self, inpt):
        """Read an utterance from your partner.

        inpt: a list of English words describing a sentence.
        """
        pass

    def write(self):
        """Generate your own utterance."""
        pass

    def choose(self):
        """Call it after the conversation is over, to make the selection."""
        pass

    def update(self, agree, reward, scale_rw = 1.0):
        """After end of each dialogue the reward will be passed back to update the parameters.

        agree: a boolean flag that specifies if the agents agreed on the deal.
        reward: the reward that the agent receives after the dialogue. 0 if there is no agreement.
        """
        pass