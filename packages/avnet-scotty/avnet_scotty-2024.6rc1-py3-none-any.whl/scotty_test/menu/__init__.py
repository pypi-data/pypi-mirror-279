# SPDX-FileCopyrightText: (C) 2023 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
"""Menu provider for scotty-test."""

import inquirer
from inquirer.themes import Default
from blessed import Terminal
from typing import Any, AnyStr, Sequence, Tuple


class AvnetTheme(Default):
    """Avnet specific theming for inquirer."""

    def __init__(self):
        """Init AvnetTheme with our own colors and symbols."""
        super().__init__()

        term = Terminal()

        self.Question.mark_color = term.color_rgb(81, 186, 117)
        self.Question.brackets_color = term.color_rgb(81, 186, 117)
        self.Question.default_color = term.normal
        self.Editor.opening_prompt_color = term.bright_black
        self.Checkbox.selection_color = term.color_rgb(81, 186, 117)
        self.Checkbox.selection_icon = "►"
        self.Checkbox.selected_icon = "[█]"
        self.Checkbox.selected_color = term.color_rgb(81, 186, 117) + term.bold
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = "[ ]"
        self.List.selection_color = term.color_rgb(81, 186, 117)
        self.List.selection_cursor = "►"
        self.List.unselected_color = term.normal


def show_menu(prompt: AnyStr, entries: Sequence[Tuple[str, Any]], multiple=False) -> Any:
    """Ask the user to make a choice in a list of possibilities."""
    if not entries:
        return ()

    theme = AvnetTheme()

    def as_list(prompt: AnyStr, entries: Sequence[Tuple[str, Any]]):
        questions = [
            inquirer.List('items',
                          message=prompt,
                          choices=entries,
                          default=entries[0],
                          carousel=True
                          )
        ]
        return inquirer.prompt(questions, theme=theme)

    def as_checklist(prompt: AnyStr, entries: Sequence[Tuple[str, Any]]):
        questions = [
            inquirer.Checkbox('items',
                              message=prompt +
                              ' (use SPACE to select, press ENTER to accept)',
                              choices=entries,
                              carousel=True
                              )
        ]
        return inquirer.prompt(questions, theme=theme)

    if multiple:
        answers = as_checklist(prompt, entries)
    else:
        answers = as_list(prompt, entries)

    return answers.get('items', None)


def show_editor(prompt: AnyStr) -> Any:
    """Ask the user to enter text information."""
    theme = AvnetTheme()
    questions = [
        inquirer.Text('items',
                      message=prompt
                      )
    ]
    return inquirer.prompt(questions, theme=theme).get('items', None)
