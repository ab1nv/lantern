from pathlib import Path
from typing import Optional

import aiohttp
from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Center, Container, Horizontal, Vertical
from textual.widgets import Input, Label, LoadingIndicator, Select, Static

from lantern.ascii_art import CAT_FRAMES, LANTERN_ASCII
from lantern.filesystem import FileSystemManager
from lantern.leetcode import LeetCodeClient
from lantern.theme import CatppuccinMocha
from lantern.utils import extract_question_slug


class AnimatedCat(Static):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_index = 0
        self.update("\n".join(CAT_FRAMES[0]))

    def on_mount(self) -> None:
        self.animate_cat()

    def animate_cat(self) -> None:
        frame = CAT_FRAMES[self.frame_index]
        self.update("\n".join(frame))
        self.frame_index = (self.frame_index + 1) % len(CAT_FRAMES)
        self.set_timer(0.5, self.animate_cat)


class FadingText(Static):
    def __init__(self, text_lines: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_lines = text_lines
        self._initial_render()

    def _initial_render(self) -> None:
        from rich.style import Style

        theme = CatppuccinMocha()
        result = Text()
        for i, line in enumerate(self.text_lines):
            opacity = max(0.3, 1.0 - (i * 0.12))
            color = theme.mauve.blend(theme.base, 1.0 - opacity)
            style = Style(color=color.hex)
            result.append(line + "\n", style=style)
        self.update(result)

    def render(self) -> Text:
        from rich.style import Style

        theme = CatppuccinMocha()
        result = Text()
        for i, line in enumerate(self.text_lines):
            opacity = max(0.3, 1.0 - (i * 0.12))
            color = theme.mauve.blend(theme.base, 1.0 - opacity)
            style = Style(color=color.hex)
            result.append(line + "\n", style=style)
        return result


class WelcomeScreen(Container):
    def compose(self) -> ComposeResult:
        with Vertical(classes="welcome-vertical"):
            with Center():
                yield FadingText(LANTERN_ASCII, classes="lantern-title")
            with Horizontal(classes="cat-container"):
                with Center():
                    yield AnimatedCat(classes="cat")
            with Center():
                yield Label(
                    "TUI to manage Leetcode solution indexes.",
                    classes="description",
                )
            with Center():
                yield Input(
                    placeholder="enter leetcode URL here",
                    classes="url-input",
                )
            with Center():
                yield Label("q: quit, enter: continue", classes="footer")
            with Center():
                yield Label(
                    "Created by Abhinav Singh. (github/ab1nv)",
                    classes="credits",
                )


class LanguageSelectScreen(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_language = None

    def compose(self) -> ComposeResult:
        with Vertical():
            with Center():
                yield Label("Select Language", classes="select-title")
            with Center():
                yield Select(
                    [
                        ("Python", "python"),
                        ("Go", "go"),
                        ("Java", "java"),
                        ("C++", "cpp"),
                    ],
                    prompt="Choose a language",
                    classes="language-select",
                )


class LoadingScreen(Container):
    def compose(self) -> ComposeResult:
        with Vertical():
            with Center():
                yield LoadingIndicator(classes="loader")
            with Center():
                yield Label("Loading...", classes="loading-text")


class LanternApp(App):
    CSS = """
    Screen {
        background: #1e1e2e;
        align: center middle;
    }
    
    .welcome-vertical {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    .lantern-title {
        height: 8;
        margin-top: 1;
        text-align: center;
        width: 100%;
    }
    
    .cat-container {
        height: 5;
        margin-top: 1;
    }
    
    .cat {
        color: #f9e2af;
        text-align: center;
    }
    
    .description {
        color: #bac2de;
        margin-top: 2;
        margin-bottom: 2;
    }
    
    .url-input {
        width: 60;
        margin-top: 2;
        margin-bottom: 1;
        border: solid #89b4fa;
    }
    
    .url-input:focus {
        border: solid #b4befe;
    }
    
    .footer {
        color: #6c7086;
        margin-top: 1;
    }
    
    .credits {
        color: #585b70;
        margin-top: 1;
    }
    
    .select-title {
        color: #cdd6f4;
        margin-top: 5;
        margin-bottom: 2;
    }
    
    .language-select {
        width: 40;
    }
    
    .loader {
        margin-top: 10;
    }
    
    .loading-text {
        color: #bac2de;
        margin-top: 2;
    }
    """

    ENABLE_COMMAND_PALETTE = False

    def __init__(self, root_dir: Path):
        super().__init__()
        self.root_dir = root_dir
        self.url: Optional[str] = None
        self.language: Optional[str] = None
        self.problem_data: Optional[dict] = None
        self.fs_manager = FileSystemManager(root_dir)
        self.leetcode_client = LeetCodeClient()

    def compose(self) -> ComposeResult:
        yield WelcomeScreen()

    def on_mount(self) -> None:
        self.fs_manager.initialize()
        welcome = self.query_one(WelcomeScreen)
        input_widget = welcome.query_one(Input)
        input_widget.focus()

    @on(Input.Submitted, ".url-input")
    def handle_url_submit(self, event: Input.Submitted) -> None:
        url = event.value.strip()
        if not url:
            return

        slug = extract_question_slug(url)
        if not slug:
            self.notify("Invalid LeetCode URL", severity="error")
            return

        self.url = url
        self.switch_to_language_select()

    @on(Select.Changed, ".language-select")
    def handle_language_change(self, event: Select.Changed) -> None:
        if event.value != Select.BLANK:
            self.language = event.value
            self.switch_to_loading()

    def switch_to_language_select(self) -> None:
        self.mount(LanguageSelectScreen(), before=self.query_one(WelcomeScreen))
        self.query_one(WelcomeScreen).remove()
        select_widget = self.query_one(Select)
        select_widget.focus()

    def switch_to_loading(self) -> None:
        self.mount(LoadingScreen(), before=self.query_one(LanguageSelectScreen))
        self.query_one(LanguageSelectScreen).remove()
        self.fetch_and_process()

    @work(exclusive=True)
    async def fetch_and_process(self) -> None:
        if not self.url or not self.language:
            return

        slug = extract_question_slug(self.url)
        if not slug:
            self.notify("Invalid URL", severity="error")
            return

        async with aiohttp.ClientSession() as session:
            self.problem_data = await self.leetcode_client.fetch_problem_data(
                session, slug
            )

        if not self.problem_data:
            self.notify("Failed to fetch problem data", severity="error")
            return

        self.process_problem()

    def process_problem(self) -> None:
        if not self.problem_data or not self.language:
            return

        question_folder = self.fs_manager.ensure_question_folder(
            self.problem_data["question_id"], self.problem_data["question_slug"]
        )
        self.fs_manager.ensure_question_readme(question_folder, self.problem_data)
        self.fs_manager.ensure_solution_file(question_folder, self.language)
        self.fs_manager.update_readme_table(self.problem_data, self.language)

        self.notify("Problem added successfully!", severity="success")
        self.exit()

    def on_key(self, event) -> None:
        if event.key == "q":
            self.exit()
        elif event.key == "ctrl+c":
            self.exit()

    def action_quit(self) -> None:
        self.exit()

    def on_unmount(self) -> None:
        pass


def run_tui(root_dir: Path) -> None:
    app = LanternApp(root_dir)
    app.run()
