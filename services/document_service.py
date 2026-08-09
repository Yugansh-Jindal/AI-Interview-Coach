import os

UPLOAD_FOLDER = "uploads"


def get_user_folder(user_id: int):

    folder = os.path.join(
        UPLOAD_FOLDER,
        f"user_{user_id}"
    )

    os.makedirs(folder, exist_ok=True)

    return folder


def get_resume_path(user_id: int):

    return os.path.join(
        get_user_folder(user_id),
        "resume.pdf"
    )


def get_job_description_path(user_id: int):

    return os.path.join(
        get_user_folder(user_id),
        "job_description.pdf"
    )


def save_resume(user_id, uploaded_file):

    path = get_resume_path(user_id)

    with open(path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return path


def save_job_description(user_id, uploaded_file):

    path = get_job_description_path(user_id)

    with open(path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return path


def documents_exist(user_id):

    return (

        os.path.exists(get_resume_path(user_id))

        and

        os.path.exists(get_job_description_path(user_id))

    )