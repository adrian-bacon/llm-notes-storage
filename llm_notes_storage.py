"""
title: LLM Notes Storage
author: adrian-bacon
author_url: https://github.com/adrian-bacon
git_url: https://github.com/adrian-bacon/llm-notes-storage
description: A set of functions to give an LLM the ability to store and retrieve notes via supported LLM tool calling or function calling.
version: 1.0.0
license: MIT
"""

import os
from pathlib import Path
import json
from pydantic import BaseModel

# If this path does not work for you, modify it as needed.  This is initially
# set assuming open webui running in a docker container.  When creating your
# open-webui docker container, you should ideally map this path to a local
# path on the system you're running open-webui on with the -v option so that
# your notes are accessible outside of the docker container.
BASE_PATH = "/app/backend/data/.llm_notes_storage"


def create_base_path() -> None:
    """
    Creates the base path for all LLM notes storage files.
    """
    Path(BASE_PATH).mkdir(parents=True, exist_ok=True)


def sanitize_title(title: str) -> str:
    """
    Sanitizes a title by removing any markdown header characters and leading and
    trailing white spaces.

    Args:
        title (str): The title of the note.

    Returns:
        str: The sanitized title.
    """
    return title.replace('#', ' ').strip()

def get_note_path(title: str) -> str:
    """
    Get the path to a note by its title.

    Args:
        title (str): The title of the note.

    Returns:
        str: The path to the note.
    """
    cleaned_title = sanitize_title(title).replace(' ', '_').lower()
    return os.path.join(BASE_PATH, f"{cleaned_title}.json")


class Tools:
    class Valves(BaseModel):
        pass

    class UserValves(BaseModel):
        pass

    def __init__(self):
        try:
            # Create the base path if it doesn't exist
            create_base_path()

        except PermissionError as e:
            print(f"ERROR: Could not create notes directory. Exception message: {str(e)}")

    def save_note(self, title: str, content: str) -> str:
        """
        Save the given note to disk. If a note with the same title already
        exists, its contents will be overwritten with the new contents;
        otherwise, a new note will be created.

        Example Usage from a prompt:
            "save that as a note titled 'test note'"
            "save this as a note called 'test note'"
            "add this to my notes under the title 'example note'"
            "add this to my notes with the title 'example note'"
            "add this to my notes titled 'example note'"
            "add this to my notes titled 'example note'"
            "save the note"
            "save this note"

        Args:
            title (str): The title of the note with no markdown formatting.
            content (str): The new content for the note.

        Returns:
            str: A SUCCESS: or ERROR: message.
        """
        try:
            create_base_path()
            if title is None or title.strip() == "":
                raise ValueError("Title cannot be an empty string, please"
                                 " generate a title that describes the contents"
                                 " of the note first.  Use `list_notes_titles`"
                                 " to get a list of existing titles to"
                                 " avoid accidentally overwriting an existing"
                                 " note.")

            with open(get_note_path(title), "w") as f:
                json.dump({"title": sanitize_title(title), "content": content}, f)

            return f"SUCCESS: Note '{title}' saved."

        except Exception as e:
            return f"ERROR: Could not save note. Exception message: {str(e)}"

    def list_all_notes(self) -> str:
        """
        Get a list of all the notes and their contents saved in the notes store.

        Example Usage from a prompt:
            "what are my notes about?"
            "show me the titles and contents of all my notes"

        Returns:
            str: A string containing the titles and contents of all notes.
        """
        try:
            create_base_path()
            notes = []
            for file in os.listdir(BASE_PATH):
                if file.endswith(".json"):
                    with open(os.path.join(BASE_PATH, file), "r") as f:
                        data = json.load(f)
                        notes.append({
                            "filename": file,
                            "title": data["title"],
                            "content": data["content"]})

            return json.dumps(notes)

        except Exception as e:
            return f"ERROR: Could not list notes.  Exception message: {str(e)}"

    def delete_note(self, title: str) -> str:
        """
        Delete a note by its title when the user asks you to.

        When an LLM calls this function to delete a note by its title, it can
        call the function `list_note_titles` to get the current list of titles
        and verify that the note was actually deleted.

        Example Usage from a prompt:
            "delete the note titled 'test note'"
            "delete the note called 'test note'"
            "remove this note called 'example note'"
            "get rid of the note with the title 'my note'"

        Args:
            title (str): The title of the note to delete.

        Returns:
            str: A SUCCESS: or ERROR: message.
        """
        try:
            create_base_path()
            note_path = get_note_path(title)

            if not os.path.exists(note_path):
                raise ValueError(f"ERROR: Note '{title}' does not exist")

            os.remove(note_path)

            return f"SUCCESS: Note '{title}' deleted."
        except Exception as e:
            return f"ERROR: Could not delete note. Exception message: {str(e)}"

    def get_note(self, title: str) -> str:
        """
        Get a note by its title and return the contents of the note to the user.

        An LLM may call this function while trying to fulfill a user prompt
        request by first calling `list_note_titles` to see if any saved notes
        might have relevant information, then call this function with the
        relevant note title to the contents of the note to help it give a
        better prompt response.

        Example Usage from a prompt:
            "what is the content of the note titled 'test note'?"
            "show me the contents of the note called 'example note'"
            "get the text of the note with the title 'my note'"
            "get note with the title 'my note'"
            "get note called 'example note'"

        Args:
            title (str): The title of the note to get.

        Returns:
            str: A JSON object containing the title and content of the note.
        """
        try:
            if title is None or title.strip() == "":
                raise ValueError("Title cannot be an empty string, please"
                                 " use `list_notes_titles` to get a list of"
                                 " existing titles to select from.")
            create_base_path()
            note_path = get_note_path(title)
            if not Path(note_path).exists():
                raise ValueError(f"ERROR: Note '{title}' does not exist")

            with open(note_path, "r") as f:
                return f.read()

        except Exception as e:
            return f"ERROR: Could not get note. Exception message: {str(e)}"

    def list_note_titles(self) -> str:
        """
        Get a list of all note titles save in the notes store.

        An LLM can call this method to see if any notes saved may contain
        information that is related to a user prompt, and if so, retrieve the
        note contents by the note title using the `get_note` function to help
        it return better results to the user.

        Example Usage from a prompt:
            "what are the titles of my notes?"
            "show me the titles of all my notes"
            "list the titles of the notes I have saved"
            "list all my notes"

        Returns:
            str: A JSON object containing a list of note titles.
        """
        try:
            create_base_path()
            titles = []
            for file in os.listdir(BASE_PATH):
                if file.endswith(".json"):
                    with open(os.path.join(BASE_PATH, file), "r") as f:
                        titles.append(json.load(f)["title"])

            return json.dumps(titles)

        except Exception as e:
            return f"ERROR: Could not list note titles.  Exception message: {str(e)}"
