from enum import Enum


class ProviderType(Enum):
    AZURE = 'azure'
    OPENAI = 'openai'
    GOOGLE = 'google'


class ModelType(Enum):
    LLM = 'llm'
    EMBEDDINGS = 'embeddings'