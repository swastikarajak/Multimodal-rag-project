from src.generator import generate_answer


def main():
    question = "What is machine learning?"

    context = """
    Machine Learning is a subset of Artificial Intelligence
    that allows systems to learn patterns from data.
    """

    answer = generate_answer(
        question=question,
        context=context
    )

    print("Question:")
    print(question)

    print("\nGenerated Answer:")
    print(answer)


if __name__ == "__main__":
    main()