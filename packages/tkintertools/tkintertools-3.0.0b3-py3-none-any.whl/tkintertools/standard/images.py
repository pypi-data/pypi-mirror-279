"""All standard Images"""

from ..core import virtual

__all__ = [
    "StillImage",
]


class StillImage(virtual.Image):
    """A simple still image"""

    # @typing.override
    def display(self) -> None:
        self.items.append(self.widget.master.create_image(
            *self.center(), image=self.image))
