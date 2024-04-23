import json
from openai import OpenAI
from openai._exceptions import OpenAIError, APIStatusError, APITimeoutError, APIResponseValidationError
from django.conf import settings


def evaluate_submission(desc, answer, explain, submission):
    # Initialize the return values to None or sensible defaults
    grade, tip = None, None
    # breakpoint()
    try:
        client = OpenAI(api_key=settings.OPENAI_SECRET_KEY)
        assistant = client.beta.assistants.create(
            instructions='You are a patient, gentle and kind software engineer interview expert, review my submission based on question info.',
            model='gpt-4-turbo-preview',
            tools=[{
                'type': 'function',
                'function': {
                    'name': 'reviewSubmission',
                    'description': 'You are a patient, gentle and kind software engineer interview expert, review my submission based on question info',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'grade': {'type': 'string', 'description': 'Quality of user submission answer', 'enum': ['Excellent', 'Good', 'Fair', 'Weak']},
                            'tip': {'type': 'string', 'description': 'If my submission is wrong. How can I improve the submission answer? explain using bullet points and limit to 120 words.'}
                        },
                        'required': ['grade', 'tip']
                    }
                }
            }]
        )
        thread = client.beta.threads.create()
        content = ('Here is Question desc: ' + desc + '\nAnswer: ' + answer
                + '\nExplain: ' + explain + '\nThis is my submission answer: ' + submission
                + '\nreview my submission based on question desc, answer and explain')
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=content
        )
        run = client.beta.threads.runs.create_and_poll(
          thread_id=thread.id,
          assistant_id=assistant.id,
          instructions=""
        )
        required_action = run.required_action
        tool_calls = required_action.submit_tool_outputs.tool_calls
        tool_call_arguments = tool_calls[0].function.arguments
        arguments_dict = json.loads(tool_call_arguments)
        grade = arguments_dict['grade']
        tip = arguments_dict['tip']
    except APITimeoutError:
        print("The request to OpenAI timed out. Please try again later.")
    except OpenAIError as e:
        print(f"An API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return grade, tip
