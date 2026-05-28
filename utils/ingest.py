from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import FAISS

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

import os

docs = []

folder_path = "documents"

# LOAD DOCUMENTS

for file in os.listdir(folder_path):

    file_path = f"{folder_path}/{file}"

    filename = file.lower()

    loaded_docs = []

    # TXT FILES

    if file.endswith(".txt"):

        loader = TextLoader(file_path)

        loaded_docs = loader.load()

    # PDF FILES

    elif file.endswith(".pdf"):

        loader = PyPDFLoader(file_path)

        loaded_docs = loader.load()

    else:

        continue

    # ADD METADATA

    for doc in loaded_docs:

        # DEPARTMENT DETECTION

        if any(word in filename for word in [
            "risk",
            "fraud",
            "vendor"
        ]):

            doc.metadata["department"] = "Risk"

        elif any(word in filename for word in [
            "compliance",
            "aml",
            "kyc",
            "sanctions"
        ]):

            doc.metadata["department"] = "Compliance"

        elif any(word in filename for word in [
            "it",
            "security",
            "cyber",
            "infrastructure"
        ]):

            doc.metadata["department"] = "IT"

        else:

            doc.metadata["department"] = "General"

        # ADD SOURCE FILE

        doc.metadata["source_file"] = file

    docs.extend(loaded_docs)

# CHUNKING

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

split_docs = splitter.split_documents(docs)

# EMBEDDINGS

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# VECTOR DATABASE

vectorstore = FAISS.from_documents(
    split_docs,
    embeddings
)

# SAVE VECTORSTORE

vectorstore.save_local("vectorstore")

print(f"Documents indexed successfully: {len(split_docs)} chunks created")