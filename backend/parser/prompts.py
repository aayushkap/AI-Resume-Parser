def get_extract_info_prompt():
    return f"""Extract information from the given resume and present it only in the following format. Only include the bullet point followed by the response.\n
    1. Name of person (Name only, no other text)
    2. Years of experience (Return only a number. No other text.)
    3. Highest degree of education (Choose from the following: High School, Bachelor's, MBA, PHD. Return only from these options)
    4. A short summary of the persons skills and work history (in a paragraph).
    """


def get_job_description_prompt(query):

    return f"""Given is the summary of a persons resume. Would this person be qualified for a job with this job description: '{query}' ? 
    All job requirements *must* be met by the summary of the persons resume.
    If any criteria within the job description are not met by the person, return No. 
    If all criteria are met, return Yes.
    Return only Yes or No.
    """
