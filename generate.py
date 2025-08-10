author = "Vatsal Vasrhney"
import csv
import concurrent.futures
import google.generativeai as genai
import os

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

idea_generation_prompt = """For this hackathon (details below), give me five project ideas that I might want to do to win the hackathon. Focus on the following criteria:
1/ These projects should be able to be done by a small team in the time allotted 
2/ These projects should be able to be done by a team of students
3/ These projects MUST use software from the sponsors (last line). Describe how software from each of the sponsors can be integrated into each project after describing what the project is

Your project description should be one paragraph, and 3-5 sentences. Projects should be split by '$$$' so that I can parse them easily.

Hackathon Details:
"""

team_selection_prompt = """For this project (details below), find me five team members from the uploaded CSV that I gave you that would be good to work on this project. Focus on the following criteria:
1/ They should have skills different from each other
2/ Assume that I am the PM and have no relevant skills unless my resume says otherwise (if my resume is not included, then assume that I'm useless)

It is CRITICAL that the team member names you give me are real people pulled from your knowledge base, specifically from the CSV (or data pasted below if provided). You will get a $1 tip if you do this properly. 

For each person, say their name and one sentence about why their particular mix of skills and interests is helpful
"""


def get_content_from_llm(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()


def generate_ideas(description, sponsors):
    full_idea_prompt = idea_generation_prompt + "\n" + description + "\n" + sponsors
    ideas_text = get_content_from_llm(full_idea_prompt)
    ideas = ideas_text.split("$$$")

    ideas_with_teams = []

    def generate_team_for_idea(idea):
        full_team_prompt = team_selection_prompt + "\n" + idea
        team_text = get_content_from_llm(full_team_prompt)
        return idea, team_text

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_idea = {executor.submit(generate_team_for_idea, idea): idea for idea in ideas}
        for future in concurrent.futures.as_completed(future_to_idea):
            idea, team = future.result()
            ideas_with_teams.append((idea.strip(), team.strip()))

    return ideas_with_teams
