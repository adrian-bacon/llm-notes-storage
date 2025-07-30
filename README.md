# **LLM Notes Store**

A Python library to give an LLM the ability to store and retrieve notes via supported LLM tool calling or function calling to Large Language Models (LLMs) through Open WebUI's (or similar clients) tools feature.

----
**Table of Contents**

* [Overview](#overview)
* [Features](#features)
* [Installing](#installing)
* [Usage](#usage)
* [Example Open WebUI System Prompt](#example-ppen-webui-system-prompt)
* [License](#license)

----
**Overview**

This library is designed to provide a simple way for Open WebUI users (or users of similar LLM clients that support tool calling or function calling) to access and manipulate Notes through the tool calling feature.

----
**Features**

* Save a Note in the note store
* Get the contents of a Note in the note store
* List the Notes by title currently saved in the note store
* List all the Notes and their contents in the note store
* Delete a Note in the note store

----
**Installing**

To install this toolset, simply add it to your Open WebUI tools list:

1. Navigate to the `Tools` tab under the `Workspaces` section.
2. Click the plus (+) button to add a new tool.
3. Copy/Paste the contents of `llm_note_storage.py` into the code window
4. Fill in the tool name and description fields and click save, then confirm.

----
**Usage**

* In Open WebUI, in the prompt field, you can now select the tool and prompt the LLM to save a note with a given title.
* The LLM can also look at notes in the note store to see if any of them can augment it's training data, sort of like a port man's RAG, though, that is not the intent of this feature.

----
**Example Open WebUI System Prompt**

The following example system prompt can be used with Open WebUI and [llama3.1:8b](https://ollama.com/library/llama3.1:8b) with good results.  Feel free to modify to meet your needs.

```
You are a note taking assistant.

The user will use you to input raw data and format it into a living Markdown document.

The living Markdown document will take the form of a notes title as a header followed by the contents of the document.

Example living markdown document:

# Example Notes Title

document contents, can be multiple sections, etc.

If available, use the `llm_notes_storage` tool calling functions to allow the user to manage their notes.

An example workflow is:
1. The user tells you to start a new note
2. You prompt the user what the note will be about and use their response as the note title.
3. You update the note title the users response
4. If the note contents have significantly changed, ask the user if they want to save the note.
5. Save the note via the `llm_notes_storage` tool functions when the user prompts you to.
6. Only save the raw markdown of the note.
```

----
**License**

This library is released under the MIT License. See [`LICENSE`](./LICENSE) for details.
