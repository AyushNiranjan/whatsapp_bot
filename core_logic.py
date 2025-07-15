from datetime import datetime
from csv import writer

# English Questions
questions_en = [
    lambda a: "What is your name?",
    lambda a: "What is your date of birth? (YYYY-MM-DD)",
    lambda a: "What is your Gender? (Male/Female/Other)",
    lambda a: "What is your residential address?",
    lambda a: "What is job search location?",
    lambda a: "What is your experience level? (Fresher/Experienced)",
    lambda a: "What is your experience company name?" if a[5].lower() == 'experienced' else "What is your highest education?",
    lambda a: "What is your experience job title?" if a[5].lower() == 'experienced' else "What is the name of your institute?",
    lambda a: "What is your experience salary?" if a[5].lower() == 'experienced' else "What is the name of your course?",
    lambda a: "What is your experience start year?" if a[5].lower() == 'experienced' else "What was your course start year?",
    lambda a: "What is your experience end year?" if a[5].lower() == 'experienced' else "What was your course end year?",
    lambda a: "What is your highest education?" if a[5].lower() == 'experienced' else "What is your English proficiency level? (Basic/Intermediate/Fluent)",
    lambda a: "What is your name of institute?" if a[5].lower() == 'experienced' else None,
    lambda a: "What is name of course?" if a[5].lower() == 'experienced' else None,
    lambda a: "What was your course start year?" if a[5].lower() == 'experienced' else None,
    lambda a: "What was your course end year?" if a[5].lower() == 'experienced' else None,
    lambda a: "What is your English proficiency level? (Basic/Intermediate/Fluent)" if a[5].lower() == 'experienced' else None,
]

# Hindi (Hinglish) Questions
questions_hi = [
    lambda a: "Aapka naam kya hai?",
    lambda a: "Aapki date of birth kya hai? (YYYY-MM-DD)",
    lambda a: "Aapka gender kya hai? (Male/Female/Other)",
    lambda a: "Aapka address kya hai?",
    lambda a: "Aap job kis location mein dhoond rahe ho?",
    lambda a: "Aapka experience level kya hai? (Fresher ya Experienced)",
    lambda a: "Aapki company ka naam?" if a[5].lower() == 'experienced' else "Aapki highest education kya hai?",
    lambda a: "Aapka job title kya tha?" if a[5].lower() == 'experienced' else "Aapke institute ka naam kya hai?",
    lambda a: "Aapki salary kitni thi?" if a[5].lower() == 'experienced' else "Course ka naam kya hai?",
    lambda a: "Job start year kya tha?" if a[5].lower() == 'experienced' else "Course start year kya tha?",
    lambda a: "Job end year kya tha?" if a[5].lower() == 'experienced' else "Course end year kya tha?",
    lambda a: "Aapki highest education kya hai?" if a[5].lower() == 'experienced' else "Aapka English level kya hai? (Basic/Intermediate/Fluent)",
    lambda a: "Institute ka naam kya tha?" if a[5].lower() == 'experienced' else None,
    lambda a: "Course ka naam kya tha?" if a[5].lower() == 'experienced' else None,
    lambda a: "Course start year kya tha?" if a[5].lower() == 'experienced' else None,
    lambda a: "Course end year kya tha?" if a[5].lower() == 'experienced' else None,
    lambda a: "English proficiency level kya hai? (Basic/Intermediate/Fluent)" if a[5].lower() == 'experienced' else None,
]

user_state = {}

def get_next_message(user_id, user_msg):
    state = user_state.get(user_id)

    if not state:
        user_state[user_id] = {"step": -1, "answers": [], "language": None}
        return "Choose your language:\n1. English\n2. Hindi", False

    if state["step"] == -1:
        if user_msg.strip() == "1":
            state["language"] = "en"
        elif user_msg.strip() == "2":
            state["language"] = "hi"
        else:
            return "Please reply with 1 for English or 2 for Hindi", False
        state["step"] = 0
        return get_question(state, []), False

    step = state["step"]
    lang = state["language"]
    msg = user_msg.strip()

    try:
        match step:
            case 0:  # Name
                if not msg.replace(" ", "").isalpha() or len(msg) < 2:
                    return get_reply(lang, "Please enter a valid name."), False

            case 1:  # DOB
                dob = datetime.strptime(msg, "%Y-%m-%d")
                age = (datetime.now() - dob).days // 365
                if age < 18:
                    return get_reply(lang, "You must be at least 18 years old to continue."), False

            case 2:  # Gender
                if msg.lower() not in ["male", "female", "other"]:
                    return get_reply(lang, "Type one of: Male, Female, or Other"), False
                msg = msg.capitalize()

            case 3 | 4:  # Address & Job location
                if len(msg) < 3:
                    return get_reply(lang, "Please enter a valid response."), False

            case 5:  # Experience
                if msg.lower() not in ["fresher", "experienced"]:
                    return get_reply(lang, "Type Fresher or Experienced"), False
                msg = msg.lower()

            case 6 | 7:  # Company / Edu fields
                if len(msg) < 2:
                    return get_reply(lang, "Please enter a valid response."), False

            case 8:  # Salary or Course
                if state["answers"][5] == "experienced":
                    if not msg.isdigit() or int(msg) < 0:
                        return get_reply(lang, "Enter salary as a number (e.g., 30000)"), False
                else:
                    if len(msg) < 2:
                        return get_reply(lang, "Please enter a valid course name."), False

            case 9 | 10 | 14 | 15:  # Years
                if not msg.isdigit() or not (1950 <= int(msg) <= datetime.now().year):
                    return get_reply(lang, "Enter a valid year (e.g., 2020)"), False

            case 11:  # Edu or English
                if state["answers"][5] == "experienced":
                    if len(msg) < 2:
                        return get_reply(lang, "Please enter your highest education."), False
                else:
                    if msg.lower() not in ["basic", "intermediate", "fluent"]:
                        return get_reply(lang, "Choose from: Basic, Intermediate, Fluent"), False
                    msg = msg.capitalize()

            case 12 | 13:
                if state["answers"][5] == "experienced" and len(msg) < 2:
                    return get_reply(lang, "Please enter a valid response."), False

            case 16:  # English level
                if msg.lower() not in ["basic", "intermediate", "fluent"]:
                    return get_reply(lang, "Choose from: Basic, Intermediate, Fluent"), False
                msg = msg.capitalize()

    except Exception:
        return get_reply(lang, "Please enter a valid input."), False

    # ✅ Save answer
    state["answers"].append(msg)

    # ➕ Go to next valid question
    next_step = step + 1
    while next_step < len(questions_en):
        q = get_question(state, state["answers"], next_step)
        if q:
            state["step"] = next_step
            return q, False
        next_step += 1

    return finish(user_id, state)

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

def finish(user_id, state):
    with open("responses.csv", "a", newline="", encoding="utf-8") as f:
        writer(f).writerow([user_id] + state["answers"])
    user_state.pop(user_id, None)
    return "✅ Thank you! Your responses have been recorded.", True
