import warnings

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)
import openai
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import pandas as pd
import os
import warnings
from Faiss.faissStuff import embed_index, get_pdf_splits
import time
from configParserService import get_from_ini


chat = ChatOpenAI(temperature=0, api_key=get_from_ini("OPEN_AI_API_KEY"))

prompt = """Extract information from the given resume and present it only in the following format. Only include the bullet point followed by the response.\n
1. Name of person (Name only, no other text)
2. Years of experience (Return only a number. No other text.)
3. Highest degree of education (Choose from the following: High School, Bachelor's, MBA, PHD. Return only from these options)
4. A short summary of the persons skills and work history (in a paragraph).
"""

# ? Final Results List
data_list = []

# ? Loop Through Resumes
for filename in os.listdir("./Resumes"):
    start_time = time.time()
    file_path = os.path.join("./Resumes", filename)

    resume = get_pdf_splits(file_path)

    resume_list = []
    for page in resume:
        resume_list.append(page.page_content)
    resume_str = ", ".join(resume_list)

    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=resume_str),
    ]

    result, content = None, None

    try:
        # result = chat(messages)
        # content = result.content
        print("")
    except Exception as e:
        print(f"General Error: {e}")

    if result and content:
        lines = content.split("\n")

        # Extracting information based on bullet points
        name = lines[0].split(". ")[1]
        experience = lines[1].split(". ")[1]
        education = lines[2].split(". ")[1]
        summary = ", ".join(lines[3].split(". ")[1:])

        """print("Name:", name)
        print("Experience:", experience)
        print("Education:", education)
        print("Summary:", summary)
        print("---")"""

        data_list.append(
            {
                "Filename": filename,
                "Name": name,
                "Experience": experience,
                "Education": education,
                "Summary": summary,
            }
        )

        # ? For Each Resume, Add to Index
        embed_index(resume, filename, "index_store")
        end_time = time.time()
        print(f"Time Taken: {end_time - start_time} seconds")

results_df = pd.DataFrame(data_list)
results_df.to_pickle("./resumeInformation.pkl")
results_df.to_csv("./resumeInformation.csv", index=False)
