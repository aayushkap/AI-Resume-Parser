"""

"""

from faiss_stuff import testEmbeddings
import pandas as pd


def handleJobDescription(query):

    # ? Load the dataframe with extracted information
    df = pd.read_pickle("./resumeInformation.pkl")

    # ? Test the embeddings for a given query
    res = testEmbeddings(query)

    # ? Create a new dataframe with the results
    result_df = pd.DataFrame(columns=df.columns)
    sources = []
    if res != None:
        for doc in res:
            # ? Extract the source of the document
            sources.append(doc.get("Metadata").get("source"))

        print("Filenames Ranked: ", sources)
        for filename in sources:
            # ? Find the row in the dataframe that matches the source in similarity search
            matching_row = df[df["Filename"] == filename]

            # result_df = pd.concat([result_df, matching_row], ignore_index=True)

            summary = matching_row["Summary"].values[0]

            messages = [
                {"role": "system", "content": summary},
            ]  # ? Important for summary to be given first.
            messages.append({"role": "user", "content": prompt})

            result = None
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages, temperature=0
                )
                result = response["choices"][0]["message"]["content"]
                print(result + " for " + filename)

                # print(len(result))
            except openai.error.OpenAIError as e:
                print(f"OpenAI Error: {e}")
            except Exception as e:
                print(f"General Error: {e}")

            if result and result == "Yes":
                result_df = pd.concat([result_df, matching_row], ignore_index=True)

    print(result_df)

    result_df.to_csv("qualifiedCandidates.csv", index=False)


if __name__ == "__main__":
    handle("Financial Analyst with a MBA in Finance. Atleast 10 years of experience.")
else:
    # ? Module Test
    handle("Financial Analyst with a MBA in Finance. Atleast 10 years of experience.")
