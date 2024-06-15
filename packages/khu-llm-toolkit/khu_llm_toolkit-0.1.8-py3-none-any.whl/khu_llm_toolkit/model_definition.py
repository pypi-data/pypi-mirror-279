import os
import configparser
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from khu_llm_toolkit.commons import ProviderType, ModelType


class ModelDefinition(object):
    """
    A class that represents an LLM definition.

    Args:
      provider: The name of the LLM provider.
    """

    def __init__(self, config_file_path: str):
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"config file '{config_file_path}' does not exist.")
        self.config_file_path = config_file_path
        self.models = self.__parse_ini_file()

    def __parse_ini_file(self):
        config = configparser.ConfigParser()
        config.read(self.config_file_path)

        models = {}
        for section in config.sections():
            group_dict = {}
            for option, value in config[section].items():
                group_dict[option] = value
            models[section] = group_dict

        # for section, group_dict in models.items():
        #     print(f"[{section}]")
        #     for option, value in group_dict.items():
        #         print(f"{option} = {value}")

        return models

    def __repr__(self):
        return "LmDefinition(config_file={})".format(self.config_file_path)

    def get_model(self, id: str, **kwargs):
        model_dict = self.models[id]
        model_type = ModelType(model_dict['type'])
        if model_type == ModelType.LLM:
            return self.__get_llm(model_dict, **kwargs)
        else:
            return self.__get_embeddings(model_dict, **kwargs)

    def __get_llm(self, model_dict, **kwargs):
        provider_type = ProviderType(model_dict['provider'])
        if provider_type == ProviderType.AZURE:
            return self.__azure_llm(model_dict, **kwargs)
        if provider_type == ProviderType.OPENAI:
            return self.__openai_llm(model_dict, **kwargs)
        if provider_type == ProviderType.GOOGLE:
            return self.__google_llm(model_dict, **kwargs)

    def __get_embeddings(self, model_dict, **kwargs):
        provider_type = ProviderType(model_dict['provider'])
        if provider_type == ProviderType.AZURE:
            return AzureOpenAIEmbeddings(openai_api_key=model_dict["api_key"],
                                         openai_api_version=model_dict["api_version"],
                                         azure_endpoint=model_dict["api_base"],
                                         deployment=model_dict["embeddings_model"])
        if provider_type == ProviderType.OPENAI:
            return OpenAIEmbeddings(openai_api_key=model_dict["api_key"])
        if provider_type == ProviderType.GOOGLE:
            os.environ["GOOGLE_API_KEY"] = model_dict["api_key"]
            return GoogleGenerativeAIEmbeddings(model=model_dict["embeddings_model"])

    def __azure_llm(self, model_dict, **kwargs):
        kwargs['azure_deployment'] = model_dict["completions_model"]
        return AzureChatOpenAI(openai_api_key=model_dict["api_key"],
                               openai_api_type='azure',
                               openai_api_version=model_dict["api_version"],
                               azure_endpoint=model_dict["api_base"],
                               **kwargs)

    def __openai_llm(self, model_dict, **kwargs):
        kwargs['model_name'] = model_dict["completions_model"]
        return ChatOpenAI(openai_api_key=model_dict["api_key"], **kwargs)

    def __google_llm(self, model_dict, **kwargs):
        return ChatGoogleGenerativeAI(google_api_key=model_dict["api_key"],
                                      model=model_dict["completions_model"],
                                      **kwargs)

    @staticmethod
    def __reset_env():
        key_list = [k for k in dict(os.environ).keys() if 'OPENAI' in k]
        for key in key_list:
            os.environ.pop(key)


if __name__ == '__main__':
    llm_def = ModelDefinition(config_file_path="config.ini")
    llm = llm_def.get_model('google-gai-gemini')
    embeddings =  llm_def.get_model('google-gai-embeddings')
    text = "This is a test query."
    print(embeddings.embed_query(text))
