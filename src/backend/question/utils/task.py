import json
import random

class Task:
    '''
    Every exercise is a task, we can build a task
    using multiple quesitons and requirements, For example:
    '''
    def __init__(self, state, category, method):
        self.state = state
        self.method = method
        self.category = category

    def to_json(self):
        return json.dumps(self.__dict__)


class Step:
    def __init__(self):
        self.data = dict()

    def build_question_step(self, question, requirement):
        self.data['question'] = question
        self.data['requirement'] = requirement


def HITE(question_lst):
    '''
    Total: 70 minutes
    Use 20 minutes to solve first question
    5 minutes break
    Use 20 minutes to solve second question
    5 minutes break
    Use 20 minutes to learn from the solution
    '''
    # Get 2 coding question base on user
    question_lst = get_recommend_question(user, 2, question_lst)
    # Build 
    step1 = Step(
        type='question', duration=20, question=question_lst[0],
        requirement=['quality', 'time_space', 'expected_length'])
    step2 = Step(type='break', duration=5)
    step3 = Step(
        type='question', duration=20, question=question_lst[1],
        requirement=['quality', 'time_space', 'expected_length'])
    step4 = Step(type='break', duration=5)
    step5 = Step(type='break', duration=20)
    task.step = [step1, step2, step3, step4, step5]
    return task


def get_category(count):
    lst =['Binary Search', 'Binary Tree', 'Hash Table', 'BFS', 'DFS']
    random.shuffle(lst)
    return lst[:count]


def get_practice_method(count):
    lst =['HITE', 'PIE', 'BE']
    random.shuffle(lst)
    return lst[:count]


def get_task(ability, state, count):
    '''
    TODO: use ability later
    '''
    lst = []
    category = get_category(count)
    method = get_practice_method(count)
    for i in range(count):
        task = Task(state, category[i], method[i])
        lst.append(task)
    return lst


def generate_task(state='new', type='classic', method='HITE'):
    task = Task.objects.get(user=user.id)
    ques_lst = Submission.objects.filter(user=user.id)
    # Fliter question based on requirement
    if method == 'HITE':
        return HITE(ques_lst)
    elif method == 'PIE':
        return PIE(ques_lst)
    elif method == 'BE':
        return BE(ques_lst)

