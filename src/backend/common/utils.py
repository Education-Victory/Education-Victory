import numpy as np
from datetime import datetime, timedelta


def cal_score(user_ability, solution_ability, user_submissions, metadata={
    "submission_frequency": 0,
    "is_review_mode": False
}):
    ### PREDEFINED CONSTANT FOR ADJUSTING SUGGESTION ALGORITHM ###
    W1 = 1
    W2 = 1
    W3 = 1
    W4 = 1
    # FORMULA OF CALCULATION
    # SL = - W1 * AL - W2 * CW + W3 * SW + W4 * RW
    ### END PREDEFINED CONSTANT ##################################

    # calculate the score base on input
    # AL
    # Define the adjust level here
    CONSTANT_AL = 5
    user_ability = np.asanyarray(user_ability)
    solution_ability = np.asanyarray(solution_ability)
    AL = ((user_ability + CONSTANT_AL *
           (np.ones(user_ability.shape))) - solution_ability)

    # CW
    # Getting user submission for this solution, ordered by time created DESC
    CONSTANT_CW = 1
    if user_submissions.count() == 0:
        CW = 0
    else:
        # Completeness by all different aspects of the latest submission
        completeness_obj = user_submissions.first().completeness
        if completeness_obj:
            cw_raw = sum([(1 if item else 0)
                          for item in completeness_obj]) / len(completeness_obj)
            CW = int(cw_raw) * CONSTANT_CW
        else:
            CW = 0

    # SW
    CONSTANT_SW_1 = 1
    CONSTANT_SW_2 = 0.3
    last_submission_date = user_submissions.first().created_at.date() if (
        user_submissions.count() > 0) else float('inf')
    date_elapsed = abs(
        (datetime.now().date() - last_submission_date).days)
    SW = CONSTANT_SW_1 * (1-np.exp(-CONSTANT_SW_2 * date_elapsed))

    # RW
    CONSTANT_RW = 1
    if metadata['is_review_mode']:
        RW = 0
    else:
        RW = CONSTANT_RW * \
            metadata['submission_frequency'] * \
            (1 if user_submissions.count() > 0 else 0)

    SL = - W1 * AL - W2 * CW + W3 * SW + W4 * RW
    return SL
