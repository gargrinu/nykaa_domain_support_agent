from crewai.llms.base_llm import BaseLLM

class MockLLM(BaseLLM):
    """
    Deterministic mock LLM.
    """

    def __init__(self):
        super().__init__(model="mock_llm")

    def call(
        self,
        messages,
        tools=None,
        callbacks=None,
        available_functions=None
    ):
        return "Mock response generated from provided context."

    def supports_function_calling(self):
        return False

    def get_context_window_size(self):
        return 8192