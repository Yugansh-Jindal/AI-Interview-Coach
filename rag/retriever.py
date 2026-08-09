from rag.vector_store import collection


def _query(
    query: str,
    user_id: int,
    source: str,
    n_results: int = 5
):


    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where={
            "$and": [
                {"user_id": str(user_id)},
                {"source": source}
            ]
        }
    )


    documents = results.get("documents", [[]])

    if not documents or not documents[0]:
        return []

    unique_documents = []

    for document in documents[0]:
        if document not in unique_documents:
            unique_documents.append(document)

    return unique_documents


def retrieve_resume_context(
    user_id: int,
    n_results: int = 5
):
    return _query(
    query=(
        "Candidate resume, technical skills, programming languages, "
        "frameworks, tools, projects, work experience, education"
    ),
    user_id=user_id,
    source="resume",
    n_results=n_results
)


def retrieve_job_context(
    user_id: int,
    n_results: int = 5
):
    """
    Retrieve job-description-related information.
    """

    return _query(
    query=(
        "Job description, required skills, responsibilities, "
        "qualifications, technologies, requirements"
    ),
    user_id=user_id,
    source="job_description",
    n_results=n_results
)


def retrieve_combined_context(
    user_id: int,
    n_results: int = 10
):
    """
    Retrieve merged resume and job description context.
    """

    resume_context = retrieve_resume_context(
        user_id,
        n_results
    )

    job_context = retrieve_job_context(
        user_id,
        n_results
    )

    combined = []

    for chunk in resume_context + job_context:

        if chunk not in combined:
            combined.append(chunk)

    return combined