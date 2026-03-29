

class PathologyVariable:
    def __init__(self, name, questions, only_intake_evaluation=False, only_follow_up_evaluation=False):
        self.name = name
        self.questions = questions

        # should we computation these variables solely on intake\ follow-up events
        self.only_intake_evaluation = only_intake_evaluation
        self.only_follow_up_evaluation = only_follow_up_evaluation




