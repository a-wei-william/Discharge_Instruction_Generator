"""file with global variables for all modules"""

# set up env
from dotenv import load_dotenv
load_dotenv()

# global variables
path_to_resources = "./resources/"


# set up embedding transformer
from langchain.embeddings import HuggingFaceBgeEmbeddings
hf_embed = HuggingFaceBgeEmbeddings(
    model_name = "BAAI/bge-small-en", 
    model_kwargs = {"device": "cpu"}, 
    encode_kwargs = {"normalize_embeddings": True}
)