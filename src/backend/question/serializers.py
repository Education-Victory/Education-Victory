import math
from rest_framework import serializers

from common.models import UserSubmission
from .models import Question, Category, Solution, Keypoint
import numpy as np
from datetime import datetime, timedelta


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'name', 'description', 'URL', 'type',
                  'created_at', 'updated_at']


class KeypointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keypoint
        fields = ['id', 'name', 'category', 'difficulty',
                  'requirements', 'created_at', 'updated_at']


class SolutionSerializer(serializers.ModelSerializer):
    keypoint = KeypointSerializer(many=True, read_only=True)
    question_name = serializers.SerializerMethodField()
    question_des = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = ['id', 'name', 'question_name', 'question_des', 'category_name', 'category', 'answer', 'keypoint',
                  'resources', 'created_at', 'updated_at']

    def get_question_name(self, obj):
        return obj.question.name

    def get_question_des(self, obj):
        return obj.question.description

    def get_category_name(self, obj):
        return obj.category.name

    def get_suggestion_level(self, solutionObj, userObj, paramObj={
        "w1": 1, "w2": 1, "w3": 1, "w4": 1,
        "is_review_mode": False,
        "user_frequency": 0
    }):
        '''        
        :solutionObj 
            current solution object
        :userObj 
            user object that requested this event 

        ## ALL CONSTANTS STARTS WITH `CONSTANT_`   
        '''
        try:
            # AL
            # Define the adjust level here
            CONSTANT_AL = 5
            user_ability = np.asanyarray(userObj.ability_id)
            solution_ability = np.asanyarray(solutionObj.ability_id)
            AL = ((user_ability + CONSTANT_AL *
                   (np.ones(user_ability.shape))) - solution_ability)

            # CW
            # Getting user submission for this solution, ordered by time created DESC
            CONSTANT_CW = 1
            userSubmissions = UserSubmission.objects.filter(
                user_id=userObj.id, solution_id=solutionObj.id).order_by('-created_at')
            if userSubmissions.count() == 0:
                CW = 0
            else:
                cw = userSubmissions.first().details['score']
                CW = int(cw) * CONSTANT_CW if cw is not None else 0

            # SW
            CONSTANT_SW_1 = 1
            CONSTANT_SW_2 = 0.3
            last_submission_date = userSubmissions.first().created_at.date() if (
                userSubmissions.count() > 0) else float('inf')
            date_elapsed = abs(
                (datetime.now().date() - last_submission_date).days)
            SW = CONSTANT_SW_1 * (1-np.exp(-CONSTANT_SW_2 * date_elapsed))

            # RW
            CONSTANT_RW = 1
            if paramObj['is_review_mode']:
                RW = 0
            else:
                RW = CONSTANT_RW * \
                    paramObj['user_frequency'] * \
                    (1 if userSubmissions.count() > 0 else 0)

            SL = - paramObj['w1'] * AL - paramObj['w2'] * CW \
                + paramObj['w3'] * SW + paramObj['w4'] * RW
            return SL

        except Exception as e:
            print("Getting suggestion level failed: " + str(e))
            return 0


class CategorySerializer(serializers.ModelSerializer):
    keypoint = KeypointSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'weight',
                  'keypoint', 'created_at', 'updated_at']
