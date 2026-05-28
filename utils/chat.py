from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import re

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)


def extract_relevant_sentences(text, question):

    sentences = re.split(r'(?<=[.!?]) +', text)

    keywords = question.lower().split()

    relevant = []

    for sentence in sentences:

        sentence_lower = sentence.lower()

        score = 0

        for keyword in keywords:

            if keyword in sentence_lower:

                score += 1

        if score > 0:

            relevant.append((sentence, score))

    relevant.sort(key=lambda x: x[1], reverse=True)

    return [r[0] for r in relevant[:2]]


def ask_question(question, department):

    retriever = db.as_retriever(search_kwargs={"k": 5})

    docs = retriever.invoke(question)

    # FILTER BY DEPARTMENT

    if department != "All":

        docs = [
            doc for doc in docs
            if doc.metadata.get("department") == department
        ]

    if len(docs) == 0:

        return "No relevant documents found."

    summary = "## Executive Insights\n\n"

    added = set()

    for doc in docs:

        relevant_sentences = extract_relevant_sentences(
            doc.page_content,
            question
        )

        for sentence in relevant_sentences:

            clean_sentence = sentence.strip()

            if clean_sentence not in added:

                added.add(clean_sentence)

                summary += f"• {clean_sentence}\n\n"

    summary += "---\n\n"

    summary += "### Analysis Metadata\n\n"

    summary += f"- Retrieved Documents: {len(docs)}\n"

    summary += f"- Department Filter: {department}\n"

    summary += f"- Semantic Search: Enabled\n"

    return summary