from typing import Optional, Dict, List

from pinecone_plugin_interface import PineconePlugin
from .core.client import ApiClient
from .core.client.api.inference_api import InferenceApi
from .core.client.model.embed_request_inputs import EmbedRequestInputs
from .core.client.model.embed_request import EmbedRequest

from .build_parameters_dict_for_inference import build_parameters_dict_for_inference
from .version import API_VERSION

from .models import EmbeddingsList


class Inference(PineconePlugin):
    """
    The `Inference` class configures and utilizes the Pinecone Inference API to generate embeddings.

    :param config: A `pinecone.config.Config` object, configured and built in the Pinecone class.
    :type config: `pinecone.config.Config`, required
    """

    def __init__(self, config, openapi_client_builder):
        self.config = config
        self.inference_api = openapi_client_builder(ApiClient, InferenceApi, API_VERSION)

    def embed(
        self, model: str, inputs: List[str], parameters: Optional[Dict[str, str]] = None, async_req=False
    ) -> EmbeddingsList:
        """
        Generates embeddings for the provided inputs using the specified model and (optional) parameters.

        :param model: The model to use for generating embeddings.
        :type model: str, required

        :param inputs: A list of items to generate embeddings for.
        :type inputs: list, required

        :param parameters: A dictionary of parameters to use when generating embeddings.
        :type parameters: dict, optional

        :param async_req: If True, the method will return a list of futures that can be used to retrieve the results.
        :type async_req: bool, optional

        :return: EmbeddingsList object with keys `data`, `model`, and `usage`. The `data` key contains a list of
        `n` embeddings, where `n` = len(inputs) and type(n) = Embedding. Precision of returned embeddings is either 
        int16 or int32, with int32 being the default. `model` key is the model used to generate the embeddings. 
        `usage` key contains the total number of tokens used at request-time.

        Example:
        >>> in = ["Who created the first computer?"]
        >>> out = (...).create(model="multilingual-e5-large", inputs=input, parameters={"input_type": "query", "truncate": "END"})
        >>> print(out)
         [{'data': [{'index': 0, 'values': [0.2, 0.1, ...]}],
         'model': 'multilingual-e5-large',
         'usage': {'total_tokens': 15}
         }]
        """
        embeddings_inputs = [EmbedRequestInputs(text=i) for i in inputs]

        if parameters:
            embeddings_parameters = build_parameters_dict_for_inference(parameters)
            request_body = EmbedRequest(model=model, inputs=embeddings_inputs, parameters=embeddings_parameters)
        else:
            request_body = EmbedRequest(
                model=model,
                inputs=embeddings_inputs,
            )

        embeddings_list = self.inference_api.embed(embed_request=request_body, async_req=async_req)
        return EmbeddingsList(embeddings_list=embeddings_list)
