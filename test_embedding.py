from src.embedding import create_embedding


def main():

    text = """
    Artificial Intelligence is transforming many industries.
    """

    embedding = create_embedding(text)

    print("Embedding created successfully!")
    print("Vector length:", len(embedding))
    print("First 10 values:")
    print(embedding[:10])


if __name__ == "__main__":
    main()