from src.gemini_client import client


def main():

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents="Explain what Retrieval Augmented Generation is in one sentence."
    )

    print("Gemini response:")
    print(response.text)


if __name__ == "__main__":
    main()