"""parsed then embed html pages and add to vector database 
    -collection is called main_collection
"""

from _global import path_to_resources, hf_embed
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain.vectorstores import Chroma


def create_collection_from_directory_txt(directory_path, db_directory, emb_func):
    """create a new/add to collection and add all the files of .txt in the directory to the collection
    
        -collection cotains evidence from all the source from one file type (dont need to create different
            collections for different sources as they will need to use the same retriever)
    """
    doc_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap  = 200,
        separators = ["\n\n"]
    )

    # load docs
    loader = DirectoryLoader(
        path = directory_path, 
        glob = f"**/*.txt", # all files of type in directory and subdirectories
        show_progress = True,
        loader_cls = TextLoader,
    )
    docs = loader.load()

    splits = doc_splitter.split_documents(docs)

    # add source metadata
    for chunk in splits:
        chunk.metadata["source"] = chunk.metadata["source"].split("/")[-1].replace(".txt","")

    # append to collection_name in db (wont overwrite existing collection)
    db = Chroma.from_documents(
        collection_name = "main_collection",
        documents = splits,
        embedding = emb_func,
        persist_directory=db_directory
    )


def create_collection_from_directory_md(directory_path, db_directory, emb_func):
    """create a new/add to collection and add all the files of .md in the directory to the collection
    
        -collection cotains evidence from all the source from one file type (dont need to create different
            collections for different sources as they will need to use the same retriever)
    """
    headers_to_split_on = [
        ("#", "Title"),
        ("##", "Header2"),
        ("###", "Header3"),
        ("####", "Header4"),
    ]

    # load docs
    loader = DirectoryLoader(
        path = directory_path, 
        glob = f"**/*.md", # all files of type in directory and subdirectories
        show_progress = True,
        loader_cls = TextLoader,
    )
    docs = loader.load()
  
    # add to db
    count = 0
    splits = []
    for doc in docs:
        split = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on).split_text(doc.page_content)

        # add source metadata
        for chunk in split:
            chunk.metadata["source"] = doc.metadata["source"].split("/")[-1].replace(".md","")

        splits.extend(split)

        count += 1
        if count%100 == 0: # save to disk every 100 documents
            db = Chroma.from_documents(
                collection_name = "main_collection",
                documents = splits,
                embedding = emb_func,
                persist_directory=db_directory
            )
            splits = []

    print("num of files added: ", count)



if __name__ == "__main__":
    create_collection_from_directory_txt(
        directory_path = f"{path_to_resources}/wiki",
        db_directory = f"{path_to_resources}/db_wiki", 
        emb_func = hf_embed
    )

    """
    create_collection_from_directory_md(
        directory_path = f"{path_to_resources}/caringforkids",
        db_directory = f"{path_to_resources}/db", 
        emb_func = hf_embed
    )

    create_collection_from_directory_md(
        directory_path = f"{path_to_resources}/cps_statements/",
        db_directory = f"{path_to_resources}/db", 
        emb_func = hf_embed
    )
    """
