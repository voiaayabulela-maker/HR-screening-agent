import gradio as gr

def run_hr_agent(cv_text, job_description):

    if not cv_text.strip():
        return "Please paste a CV before submitting."

    if not job_description.strip():
        return "Please paste a job description before submitting."

    result = {
    "score": 80,
    "decision": "SHORTLIST",
    "matched_skills": ["Computer Literacy", "Customer Service"],
    "missing_skills": ["Attention to detail"],
    "interview_questions": ["Tell me about your admin experience?"]
}

    output = f"""
CANDIDATE SUMMARY

Match Score: {result['score']}/100

Recommendation: {result['decision']}

Strengths:
"""

    for skill in result["matched_skills"]:
        output += f"- {skill}\n"

    output += "\nGaps:\n"

    for skill in result["missing_skills"]:
        output += f"- {skill}\n"

    output += "\nInterview Questions:\n"

    for question in result["interview_questions"]:
        output += f"- {question}\n"

    output += f"\nDecision Reason: Candidate matched {len(result['matched_skills'])} key requirement(s)."

    return output



app = gr.Interface(
    fn=run_hr_agent,
    inputs=[
        gr.Textbox(lines=10, label="Paste CV"),
        gr.Textbox(lines=10, label="Paste Job Description")
    ],
    outputs="text",
    title="HR Assistant Agent 🤖",
    description="paste a candidate CV and job description to receive screening recommendation and interview guidance"
)

app.launch()

def smart_match(cv_text, required_skills):
    cv_text = cv_text.lower()

    score = 0
    matched = []
    reasons = []

    for skill, data in required_skills.items():
        for keyword in data["keywords"]:
            if keyword in cv_text:

                score += data["weight"]
                matched.append(skill)

                # reasoning layer (IMPORTANT upgrade)
                reasons.append(f"{skill} matched because CV contains '{keyword}'")

                break

    return score, matched, reason

def hr_agent(cv_text, job_description, required_skills):

    score, matched_skills, reasons = smart_match(cv_text, required_skills)

    missing_skills = [
        skill for skill in required_skills
        if skill not in matched_skills
    ]

    if score >= 70:
        decision = "SHORTLIST"
    elif score >= 40:
        decision = "REVIEW"
    else:
        decision = "REJECT"

    questions = [
        "Tell me about your experience related to this role?",
        "How do you handle administrative tasks under pressure?"
    ]

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "reasons": reasons,
        "decision": decision,
        "interview_questions": questions
    }

def run_hr_agent(cv_text, job_description):

    result = hr_agent(cv_text, job_description, required_skills)

    output = f"""
CANDIDATE SUMMARY

Match Score: {result['score']}/100

Decision: {result['decision']}

Strengths:
"""

    for skill in result["matched_skills"]:
        output += f"- {skill}\n"

    output += "\nGaps:\n"

    for skill in result["missing_skills"]:
        output += f"- {skill}\n"

    output += "\nWHY MATCHED:\n"

    for r in result["reasons"]:
        output += f"- {r}\n"

    output += "\nInterview Questions:\n"

    for q in result["interview_questions"]:
        output += f"- {q}\n"

    return output


app = gr.Interface(
    fn=run_hr_agent,
    inputs=[
        gr.Textbox(lines=10, label="Paste CV"),
        gr.Textbox(lines=10, label="Paste Job Description")
    ],
    outputs="text",
    title="HR Assistant Agent 🤖",
    description="Screen CVs, match skills, and generate interview questions"
)

app.launch()
