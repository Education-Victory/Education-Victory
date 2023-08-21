class Task:
    '''
    Every exercise is a task, we can build a task
    use multiple quesiton and requirement
    '''
    def __init__(self):
        self.task = None

    def add(self, lst):
        pass


def recommend_package(type, user):
    '''
    Recommend different exercise for user
    '''
    # High Intensity Interval Exercise
    if type == 0:
        task = HITE(user)
    # Breakthrough Practice
    elif type == 1:
        task = Breakthrough(user)
    # Review
    elif type == 2:
        task = Review(user)
    return task


def HITE(user):
    '''
    Total: 70 minutes
    Use 20 minutes to solve first question
    5 minutes break
    Use 20 minutes to solve second question
    5 minutes break
    Use 20 minutes to learn from the solution
    '''
    ability = user.ability
    first_question = recomend_question(user)
    first_question['requirement'] = code_requirement()
    time_break = time_break(5)
    second_question['requirement'] = code_requirement()
    time_break = time_break(5)
    time_break = time_break(20)
    task = Task()
    task.add([
        first_question, time_break(5), first_question,
        time_break(5), time_break(20)])
    return task


def recommend_question(user, category=None):
    '''
    Get recommend question base on user ability, category, etc.
    '''
    pass


def code_requirement(
        time=20, quality=80,
        time_space=True, expected_length=True):
    pass


def choice_requirement(time=5):
    pass

