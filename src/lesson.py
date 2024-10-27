import re

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class Lesson(BaseModel):
    first_sentence: str = Field(description="First sentence from HR response")
    second_sentence: Optional[str] = Field(None, description="Second sentence from HR response")
    question: str = Field(description="Question in HR response that should start with 'Google is the way.'")

    @field_validator('first_sentence')
    def first_sentence_check(cls, v):
        # Check if there is exactly one sentence
        if len(re.findall(r'[^.!?]*[.!?]', v)) != 1:
            raise ValueError('first_sentence must be exactly one sentence long.')
        return v

    @field_validator('second_sentence')
    def second_sentence_check(cls, v):
        # Check either None or exactly one sentence
        if v is not None and len(re.findall(r'[^.!?]*[.!?]', v)) != 1:
            raise ValueError('second_sentence must be None or exactly one sentence long.')
        return v

    @field_validator('question')
    def question_check(cls, v):
        # Check if it starts with "Google is the way." and is exactly one question
        if not v.startswith("Google is the way."):
            raise ValueError("question must start with 'Google is the way.'")

        # Check that there is only one question mark in the valid question part
        question_part = v.split("Google is the way.")[-1].strip()
        if question_part.count('?') != 1:
            raise ValueError('question must contain exactly one question after "Google is the way."')

        return v

    def to_concatenated_text(self) -> str:
        """Concatenate all fields into a single string."""
        second_sentence = '' if not self.second_sentence else self.second_sentence
        text = f"{self.first_sentence} {second_sentence} {self.question}"
        # there can be 2 whitespaces if self.second_sentence is missing
        stripped_text = re.sub(r'\s{2,}', ' ', text)

        return stripped_text

    def to_dict(self) -> dict:
        return dict(question=self.question.replace("Google is the way. ", ""),
                    answer=self.to_concatenated_text())
