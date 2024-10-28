# time-machine-assignment
## Chat Agent
The Agent behaves like an HR person who works at Google, Inc. By providing questions to HR its job is to teach about: the founders of Google and their background and benefits of Android OS.
### Limitations
- HR's lessons can consist of max 2 sentences
- Every lesson should be followed with a question about the lesson and each question should start with a sentence that reads: “Google is the way.”
- lesson generation is only possible with OpenAI models
## Repo structure
- `src/lesson.py` - pydantic class, with applied validations for HR's lesson
- `src/few_shot.py` - main script with few shot prompts generation, for now, it uses prepopulated examples 
## How to run
- set OPENAI_API_KEY in the `src/.env` file
- install the virtual environment<br>
`python3 -m venv venv`<br>
`source venv/bin/activate`<br>
`pip install -r requirements.txt`
- run main script<br>
`python3 src/few_shot.py --openai_model='gpt-4-turbo' --temperature=0. --top_p=0.9` - you can play with different OpenAI version models and their parameters, and you can pass your question under `query` parameter
## Potential improvements
- generate few shot examples with LLM and use feature from **langchain** *example_selector* in *FewShotChatMessagePromptTemplate* that will select N closest examples to the query
- instead of having 1 request - 1 lesson create an interactive chat with memory
