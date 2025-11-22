from langchain.chains import LLMChain
from langchain.llms.fake import FakeListLLM
from langchain.prompts import PromptTemplate

from app.settings import get_settings

settings = get_settings()


class Summarizer:
    """Use LangChain to summarize note content without external calls."""

    def __init__(self) -> None:
        self.prompt = PromptTemplate.from_template(
            "Summarize the following note in one sentence: {content}"
        )
        # FakeListLLM avoids network access by returning deterministic content.
        self.llm = FakeListLLM(responses=["This note discusses key ideas succinctly."])
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def summarize(self, content: str) -> str:
        if not settings.summary_enabled:
            return ""
        return self.chain.run(content=content)


summarizer = Summarizer()
