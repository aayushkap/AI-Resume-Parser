"""
Extract Information form a Resume, store in CSV and VDB.
"""

import warnings
import pandas as pdd
import os

from services import api_call
from prompts import get_extract_info_prompt

warnings.filterwarnings("ignore", category=DeprecationWarning)


def extract_info():
    # ? Final Results List
    data_list = []

    for filename in os.listdir("./Resumes"):

        file_path = os.path.join("./Resumes", filename)

        resume = get_pdf_splits(file_path)

        resume_list = []
        for page in resume:
            resume_list.append(page.page_content)
        resume_content = ", ".join(resume_list)

        result = None

        result = api_call(get_extract_info_prompt, resume_content)

        if result:
            lines = result.split("\n")

            # ? Extracting information based on bullet points
            name = lines[0].split(". ")[1]
            experience = lines[1].split(". ")[1]
            education = lines[2].split(". ")[1]
            summary = ", ".join(lines[3].split(". ")[1:])

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
            # embed_index(resume, filename, "index_store")

    results_df = pd.DataFrame(data_list)
    results_df.to_pickle("./resumeInformation.pkl")
    results_df.to_csv("./resumeInformation.csv", index=False)  # Remove
