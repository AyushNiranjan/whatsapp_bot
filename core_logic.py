from datetime import datetime
from csv import writer

questions = [
    lambda a: "What is your name?",
    lambda a: "What is your date of birth?",
    lambda a: "What is your Gender?",
    lambda a: "What is your residential address?",
    lambda a: "What is job search location?",
    lambda a: "What is your experience level?",  

    lambda a: "What is experience_company_name?" if a[5].lower() == 'experienced' else "What is your highest education?",
    lambda a: "What is your experience job title?" if a[5].lower() == 'experienced' else "What is name of institute?",
    lambda a: "What is your experience salary?" if a[5].lower() == 'experienced' else "What is name of course?",
    lambda a: "What is your start date?" if a[5].lower() == 'experienced' else "What was start year?",
    lambda a: "What was your end date?" if a[5].lower() == 'experienced' else "What was end year?",
    lambda a: "What is your highest education?" if a[5].lower() == 'experienced' else "What is your English proficiency level?",
    lambda a: "What is your name of institute?" if a[5].lower() == 'experienced' else None,
    lambda a: "What is name of course?" if a[5].lower() == 'experienced' else None,
    lambda a: "What was start year?" if a[5].lower() == 'experienced' else None,
    lambda a: "What was end year?" if a[5].lower() == 'experienced' else None,
    lambda a: "What is your English proficiency level?" if a[5].lower() == 'experienced' else None
]

user_state = {}

def get_next_message(user_id, user_msg):
    state = user_state.get(user_id)

    if not state:
        state = {"step": 0, "answers": []}
        user_state[user_id] = state
        return questions[0]([]), False

    
    if state["step"] > 0 or (state["step"] == 0 and user_msg.strip()):
        state["answers"].append(user_msg.strip())

    
    next_step = state["step"] + 1
    while next_step < len(questions):
        question_fn = questions[next_step]
        if question_fn is None:
            return finish(user_id, state)
        question = question_fn(state["answers"])
        if question is not None:
            state["step"] = next_step
            user_state[user_id] = state
            return question, False
        else:
            next_step += 1

    return finish(user_id, state)

def finish(user_id, state):
    with open("responses.csv", "a", newline="") as f:
        writer(f).writerow([user_id] + state["answers"])
    user_state.pop(user_id, None)
    return "✅ Thanks! Your response has been saved.", True
