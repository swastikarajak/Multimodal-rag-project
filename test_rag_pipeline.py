from src.rag_pipeline import answer_question


def main():
    question = "What is Machine Learning?"

    result = answer_question(
        question=question,
        n_results=2
    )

    print("================================")
    print("QUESTION")
    print("================================")
    print(question)

    print("\n================================")
    print("ANSWER")
    print("================================")
    print(result["answer"])

    print("\n================================")
    print("SOURCES")
    print("================================")

    for source in result["sources"]:
        print(
            f"File: {source['source_file']}"
        )
        print(
            f"Page: {source['page_number']}"
        )
        print(
            f"Type: {source['content_type']}"
        )
        print("--------------------------------")


if __name__ == "__main__":
    main()