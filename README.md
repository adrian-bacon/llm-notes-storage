# **LLM Notes Store**
==========================

A Python library to give an LLM the ability to store and retrieve notes via supported LLM tool calling or function calling to Large Language Models (LLMs) through Open WebUI's (or similar clients) tools feature.

**Table of Contents**
-----------------

* [Overview](#overview)
* [Features](#features)
* [Installing](#installing)
* [Usage](#usage)
* [License](#license)

**Overview**
------------

This library is designed to provide a simple way for Open WebUI users (or users of similar LLM clients that support tool calling or function calling) to access and manipulate Notes through the tool calling feature.

**Features**
------------

* Save a Note in the note store
* Get the contents of a Note in the note store
* List the Notes by title currently saved in the note store
* List all the Notes and their contents in the note store
* Delete a Note in the note store

**Installing**
---------

To install this toolset, simply add it to your Open WebUI tools list:

1. Navigate to the `Tools` tab under the `Workspaces` section.
2. Click the plus (+) button to add a new tool.
3. Copy/Paste the contents of `llm_note_store.py` into the code window
4. Fill in the tool name and description fields and click save, then confirm.

**Usage**
--------------------

* In Open WebUI, in the prompt field, you can now select the tool and prompt the LLM to save a note with a given title.
* The LLM can also look at notes in the note store to see if any of them can augment it's training data, sort of like a port man's RAG, though, that is not the intent of this feature.

**License**
----------

This library is released under the MIT License. See `LICENSE` for details.
