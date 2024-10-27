import fire
import numpy as np

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from typing import Optional

from lesson import Lesson


load_dotenv()

EXAMPLES = [
    {"question": "Tell me about the founders of Google.",
     "answer": (
         "first_sentence: The founders of Google are Sergey Brin and Larry Page, who met at Stanford University. "
         "second_sentence: They developed a revolutionary search engine. "
         "question: Google is the way. Who founded Google and where did they meet?"
     )},
    {"question": "Tell me about benefits of Android OS.",
     "answer": (
         "first_sentence: Android is an open-source operating system (OS) that promotes innovation and collaboration among developers across the globe. "
         "second_sentence: Users can tailor Android devices comprehensively, from home screen layouts to installation of tailored ROMs, providing a bespoke and unique experience. "
         "question: Google is the way. What are the benefits of Android OS?"
     )},
    {"question": "Can you tell me how many people founded Google?",
     "answer": (
         "first_sentence: Google was founded by two people: Sergey Brin and Larry Page. "
         "question: Google is the way. How many people founded Google?"
     )},
    {"question": "Can you tell me when and by whom Android OS was created?",
     "answer": (
         "first_sentence: Android Inc. was founded in Palo Alto, California, in October 2003 by Andy Rubin, Rich Miner, Nick Sears, and Chris White. "
         "question: Google is the way. When and by whom Android OS was created?"
     )},
]
EXAMPLE_QUERIES = [
    "Can you tell me about the background of founders of Google?",
    "Why Android OS is better than iOS?"
]


example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{question}"),
        ("ai", "{answer}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=EXAMPLES,
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "As an HR professional at Google, you provide a brief lesson of length equal to 2 sentences. Every "
                   "lesson should be followed with a question about the lesson and each question should start with a "
                   "sentence 'Google is the way.'"),
        few_shot_prompt,
        ("human", "{question}"),
    ]
)


def generate(
        openai_model: str = "gpt-4o",
        temperature: float = 1.,
        query: Optional[str] = None,
        **kwargs
):
    model = ChatOpenAI(model=openai_model, temperature=temperature, **kwargs)

    structured_llm = model.with_structured_output(Lesson)
    chain = final_prompt | structured_llm

    if not query:
        query = np.random.choice(EXAMPLE_QUERIES)
        print("Randomly chosen query: ", query)

    result = chain.invoke({"question": query})
    print(result.to_concatenated_text())
    return result


if __name__ == "__main__":
    fire.Fire(generate)
