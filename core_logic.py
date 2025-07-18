from flask import Flask, request
from datetime import datetime
from csv import writer
import pandas as pd
import random

# English Questions
questions_en = [
    lambda a: "What is your name?",
    lambda a: "What is your date of birth? (YYYY-MM-DD)",
    lambda a: "What is your Gender? (Male/Female/Other)",
    lambda a: "What is your residential address?",
    lambda a: "what is your job title?",
    lambda a: "What is job search location?",
    lambda a: "What is your experience level? (Fresher/Experienced)",
    lambda a: "What is your experience company name?" if a[6].lower() == 'experienced' else "What is your highest education?",
    lambda a: "What is your experience job title?" if a[6].lower() == 'experienced' else "What is the name of your institute?",
    lambda a: "What is your experience salary?" if a[6].lower() == 'experienced' else "What is the name of your course?",
    lambda a: "What is your experience start year?" if a[6].lower() == 'experienced' else "What was your course start year?",
    lambda a: "What is your experience end year?" if a[6].lower() == 'experienced' else "What was your course end year?",
    lambda a: "What is your highest education?" if a[6].lower() == 'experienced' else "What is your English proficiency level? (Basic/Intermediate/Fluent)",
    lambda a: "What is your name of institute?" if a[6].lower() == 'experienced' else None,
    lambda a: "What is name of course?" if a[6].lower() == 'experienced' else None,
    lambda a: "What was your course start year?" if a[6].lower() == 'experienced' else None,
    lambda a: "What was your course end year?" if a[6].lower() == 'experienced' else None,
    lambda a: "What is your English proficiency level? (Basic/Intermediate/Fluent)" if a[6].lower() == 'experienced' else None,
]

# Hindi (Hinglish) Questions
questions_hi = [
    lambda a: "Aapka naam kya hai?",
    lambda a: "Aapki date of birth kya hai? (YYYY-MM-DD)",
    lambda a: "Aapka gender kya hai? (Male/Female/Other)",
    lambda a: "Aapka address kya hai?",
    lambda a: "Aapko kis role mein job chahiye",
    lambda a: "Aap job kis location mein dhoond rahe ho?",
    lambda a: "Aapka experience level kya hai? (Fresher ya Experienced)",
    lambda a: "Aapki company ka naam?" if a[6].lower() == 'experienced' else "Aapki highest education kya hai?",
    lambda a: "Aapka job title kya tha?" if a[6].lower() == 'experienced' else "Aapke institute ka naam kya hai?",
    lambda a: "Aapki salary kitni thi?" if a[6].lower() == 'experienced' else "Course ka naam kya hai?",
    lambda a: "Job start year kya tha?" if a[6].lower() == 'experienced' else "Course start year kya tha?",
    lambda a: "Job end year kya tha?" if a[6].lower() == 'experienced' else "Course end year kya tha?",
    lambda a: "Aapki highest education kya hai?" if a[6].lower() == 'experienced' else "Aapka English level kya hai? (Basic/Intermediate/Fluent)",
    lambda a: "Institute ka naam kya tha?" if a[6].lower() == 'experienced' else None,
    lambda a: "Course ka naam kya tha?" if a[6].lower() == 'experienced' else None,
    lambda a: "Course start year kya tha?" if a[6].lower() == 'experienced' else None,
    lambda a: "Course end year kya tha?" if a[6].lower() == 'experienced' else None,
    lambda a: "English proficiency level kya hai? (Basic/Intermediate/Fluent)" if a[6].lower() == 'experienced' else None,
]

user_state = {}

# Load job data once
job_df = pd.read_csv("JobPost_List.csv")

def get_next_message(user_id, user_msg):
    user_msg = user_msg.strip()
    state = user_state.get(user_id)

    # 1. New user initialization
    if not state:
        user_state[user_id] = {"step": -1, "answers": [], "language": None}
        return "Choose your language:\n1. English\n2. Hindi", False

    # 2. Language selection step
    if state["step"] == -1:
        if user_msg == "1":
            state["language"] = "en"
        elif user_msg == "2":
            state["language"] = "hi"
        else:
            return "Please reply with 1 for English or 2 for Hindi", False
        state["step"] = 0
        return get_question(state, state["answers"]), False

    # 3. Fetch current step and language
    step = state["step"]
    lang = state["language"]

    # 4. Validate input
    is_valid, cleaned_msg_or_error = validate_input(step, user_msg, state["answers"], lang)
    if not is_valid:
        return get_reply(lang, cleaned_msg_or_error), False

    # 5. Store valid cleaned message
    state["answers"].append(cleaned_msg_or_error)

    # 6. Move to next step
    next_step = step + 1
    question_list = questions_en if lang == "en" else questions_hi

    while next_step < len(question_list):
        q = get_question(state, state["answers"], next_step)
        if q:
            state["step"] = next_step
            return q, False
        next_step += 1

    # 7. Finish and show jobs
    return finish(user_id, state)


def validate_input(step, msg, answers, lang):
    msg = msg.strip()

    try:
        match step:
            case 0:
                if len(msg) < 2 or not msg.replace(" ", "").isalpha():
                    return False, "Please enter a valid name."
                return True, msg.title()

            case 1:
                dob = datetime.strptime(msg, "%Y-%m-%d")
                if (datetime.now() - dob).days // 365 < 18:
                    return False, "You must be at least 18 years old to continue."
                return True, msg

            case 2:
                if msg.lower() not in ["male", "female", "other"]:
                    return False, "Type one of: Male, Female, or Other"
                return True, msg.capitalize()

            case 3 | 4 | 6 | 7:
                if len(msg) < 3:
                    return False, "Please enter a valid response."
                return True, msg

            case 5:
                if msg.lower() not in ["fresher", "experienced"]:
                    return False, "Type Fresher or Experienced"
                return True, msg.lower()

            case 8:
                if answers[5] == "experienced":
                    if not msg.isdigit() or int(msg) < 0:
                        return False, "Enter salary as a number (e.g., 30000)"
                elif len(msg) < 2:
                    return False, "Please enter a valid course name."
                return True, msg

            case 9 | 10 | 14 | 15:
                if not msg.isdigit() or not (1950 <= int(msg) <= datetime.now().year):
                    return False, "Enter a valid year (e.g., 2020)"
                return True, msg

            case 11:
                if answers[5] == "experienced":
                    if len(msg) < 2:
                        return False, "Please enter your highest education."
                elif msg.lower() not in ["basic", "intermediate", "fluent"]:
                    return False, "Choose from: Basic, Intermediate, Fluent"
                return True, msg.capitalize()

            case 12 | 13:
                if answers[5] == "experienced" and len(msg) < 2:
                    return False, "Please enter a valid response."
                return True, msg

            case 16:
                if msg.lower() not in ["basic", "intermediate", "fluent"]:
                    return False, "Choose from: Basic, Intermediate, Fluent"
                return True, msg.capitalize()

    except Exception:
        return False, "Please enter a valid input."

    return True, msg

    


def get_question(state, answers, index=None):
    lang = state["language"]
    qlist = questions_en if lang == "en" else questions_hi
    step = index if index is not None else state["step"]
    fn = qlist[step]
    return fn(answers) if fn else None

def get_reply(lang, text):
    if lang == "hi":
        return {
            "Please enter a valid name.": "Kripya sahi naam daaliye.",
            "You must be at least 18 years old to continue.": "Aapko aage badhne ke liye kam se kam 18 saal ka hona chahiye.",
            "Please enter your DOB in YYYY-MM-DD format.": "DOB format YYYY-MM-DD mein daaliye.",
            "Type one of: Male, Female, or Other": "Kripya Male, Female, ya Other mein se chunav karein.",
            "Type Fresher or Experienced": "Fresher ya Experienced mein se chunav karein.",
            "Enter salary as a number (e.g., 30000)": "Salary sirf number mein daaliye (jaise 30000).",
            "Please enter a valid course name.": "Kripya sahi course naam daaliye.",
            "Enter a valid year (e.g., 2020)": "Kripya sahi saal daaliye (jaise 2020).",
            "Choose from: Basic, Intermediate, Fluent": "Kripya Basic, Intermediate, ya Fluent mein se chunav karein.",
            "Please enter your highest education.": "Kripya apni highest education daaliye.",
            "Please enter a valid response.": "Kripya sahi response daaliye.",
            "Please enter a valid input.": "Kripya sahi input daaliye.",
        }.get(text, text)
    return text

import csv
import random

def finish(user_id, state):
    with open("responses.csv", "a", newline="", encoding="utf-8") as f:
        writer(f).writerow([user_id] + state["answers"])

    job_title = state["answers"][4].lower()
    suggestions = []

    try:
        with open("JobPost_List.csv", newline="", encoding="utf-8") as jf:
            reader = csv.DictReader(jf)
            jobs = [row for row in reader if row.get("Employer Brand Name") and row.get("Job Title")]

            # Find matches based on job title
            matches = [
                {"company": j["Employer Brand Name"], "title": j["Job Title"]}
                for j in jobs
                if job_title in j.get("Job Title", "").lower()
            ]

            # If no matches, fallback to random jobs
            pool = matches if matches else [
                {"company": j["Employer Brand Name"], "title": j["Job Title"]}
                for j in jobs
            ]

            # Pick top 3 suggestions
            suggestions = random.sample(pool, min(3, len(pool)))

    except Exception as e:
        print("Error in suggesting jobs:", e)

    # Remove user state
    user_state.pop(user_id, None)

    # Format the suggestion message
    if suggestions:
        message = "✅ Thank you! Your responses have been recorded.\n\nHere are some job opportunities:\n"
        for idx, s in enumerate(suggestions, 1):
            message += f"{idx}. {s['title']} at {s['company']}\n"
        return message.strip(), True
    else:
        return "✅ Thank you! Your responses have been recorded.", True
