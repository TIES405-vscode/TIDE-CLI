"""Provide feedback to console/IDE from TIM."""

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
__license__ = "MIT"
__date__ = "11.5.2024"

from pydantic import BaseModel


class WebData(BaseModel):
    """Data from the web response."""

    console: str | None = None
    error: str
    language: str | None = None
    pwd: str | None = None
    runtime: str | None = None


class TimFeedback(BaseModel):
    """Model for feedback response after submitting a task."""

    savedNew: int | None
    """Whether the new answer was saved."""

    valid: bool
    """Whether the answer was valid."""

    web: WebData | None
    """Data from the web response."""

    def console_output(self) -> str | list[str]:
        """Return the console output of the task."""
        if self.web is None:
            return "No response from TIM."

        if self.web.error != "":
            return self.web.error

        if self.savedNew:
            saved_new = "Saved new answer successfully."
        else:
            saved_new = "New answer was not saved.\
            Same file was already submitted."

        if self.web.console is None:
            return f"{saved_new} No console feedback from TIM."

        return f" {saved_new}\n\nFeedback from TIM: {self.web.console}"


class PointsData(BaseModel):
    """Model for task points information."""

    current_points: float | None
    """Current points awarded for answering the task"""

    def pretty_print(self) -> str:
        """
        :return: Points data in a human-readable format
        """
        return f"Current points: {self.current_points}"
