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
# set assuming open webui running in a docker container
BASE_PATH = "/app/backend/data/.llm_notes_storage"


def sanitize_title(title: str) -> str:
    """
    Sanitizes a title by removing any markdown header files and leading and 
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
            Path(BASE_PATH).mkdir(parents=True, exist_ok=True)

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
            "save the note"

        Args:
            title (str): The title of the note with no markdown formatting.
            content (str): The new content for the note.

        Returns:
            str: A success message if the note was saved successfully.
        """
        try:
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

    def list_notes(self) -> str:
        """
        Get a list of all notes.

        Example Usage from a prompt:
            "what are my notes about?"
            "list all my notes"
            "show me the titles and contents of all my notes"

        Returns:
            str: A string containing the titles and contents of all notes.
        """
        try:
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
        Delete a note by its title.

        Example Usage from a prompt:
            "delete the note titled 'test note'"
            "remove this note called 'example note'"
            "get rid of the note with the title 'my note'"

        Args:
            title (str): The title of the note to delete.

        Returns:
            str: A success message if the note was deleted successfully.
        """
        try:
            note_path = get_note_path(title)

            if not Path(note_path).exists():
                raise ValueError(f"ERROR: Note '{title}' does not exist")

            Path(note_path).unlink()

            return f"SUCCESS: Note '{title}' deleted."
        except Exception as e:
            return f"ERROR: Could not delete note. Exception message: {str(e)}"

    def get_note(self, title: str) -> str:
        """
        Get a note by its title.

        Example Usage from a prompt:
            "what is the content of the note titled 'test note'?"
            "show me the contents of the note called 'example note'"
            "get the text of the note with the title 'my note'"

        Args:
            title (str): The title of the note to get.

        Returns:
            str: A JSON object containing the title and content of the note.
        """
        try:
            note_path = get_note_path(title)
            if not Path(note_path).exists():
                raise ValueError(f"ERROR: Note '{title}' does not exist")

            with open(note_path, "r") as f:
                return f.read()

        except Exception as e:
            return f"ERROR: Could not get note. Exception message: {str(e)}"

    def list_note_titles(self) -> str:
        """
        Get a list of all note titles.

        Example Usage from a prompt:
            "what are the titles of my notes?"
            "show me the titles of all my notes"
            "list the titles of the notes I have saved"

        Returns:
            str: A JSON object containing a list of note titles.
        """
        try:
            titles = []
            for file in os.listdir(BASE_PATH):
                if file.endswith(".json"):
                    with open(os.path.join(BASE_PATH, file), "r") as f:
                        titles.append(json.load(f)["title"])

            return json.dumps(titles)

        except Exception as e:
            return f"ERROR: Could not list note titles.  Exception message: {str(e)}"
          
