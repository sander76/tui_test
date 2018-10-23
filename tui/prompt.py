import asyncio
from asyncio import CancelledError

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.eventloop import use_asyncio_event_loop
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import (
    focus_previous,
    focus_next,
)
from prompt_toolkit.layout import HSplit, BufferControl, ScrollOffsets
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Button, TextArea


class MainMenu:
    def __init__(self, loop):
        self.loop = loop
        self.log_output = TextArea(scrollbar=True)
        self.app = Application(
            full_screen=True, key_bindings=self.get_bindings()
        )

        self.root_container = VSplit(
            [
                Shades(loop, self.log_output, self).content,
                Window(width=1, char="|"),
                self.log_output,
            ]
        )
        self.app.layout = Layout(self.root_container)

    def get_bindings(self):
        kb = KeyBindings()

        @kb.add("c-q")
        def _(event):
            print("exiting")
            event.app.exit()

        return kb


class Menu:
    def __init__(self, loop, logbuffer, main, previous=None):
        self.loop = loop
        self.main = main
        # self.kb = KeyBindings()
        self._buttons = HSplit(
            self.buttons,
            key_bindings=self.get_key_bindings(KeyBindings()),
            modal=True,
        )
        self.log_buffer = logbuffer
        self.previous = previous

    def show(self, data=None):
        self.main.root_container.children[0] = self._buttons
        self.main.app.layout.focus(self._buttons)

    def print(self, item, newline=True):
        if newline:
            self.log_buffer.text = "{}{}\n".format(self.log_buffer.text, item)
            return
        self.log_buffer.text = "{}{}".format(self.log_buffer.text, item)

    @property
    def content(self):
        return self._buttons

    def back(self, *args):
        if self.previous:
            self.previous.show()

    @property
    def buttons(self):
        return []

    def get_key_bindings(self, kb):
        kb.add("up")(focus_previous)
        kb.add("down")(focus_previous)
        kb.add("b")(self.back)
        return kb


def shades():
    val = None

    while 1:
        pass

    return val


class Shades(Menu):
    @property
    def buttons(self):
        return [
            Button("select shade 1", handler=self.command_1),
            Button("command_2", handler=self.command_2),
        ]

    def get_key_bindings(self, kb):
        kb.add("c-s")(self.command_1)
        return super().get_key_bindings(kb)

    def command_1(self, *args):
        other = OtherContext(
            self.loop, self.log_buffer, self.main, previous=self
        )
        other.show()

    def command_2(self, *args):
        self.print("command 2")


class Entry(Menu):
    pass


class OtherContext(Menu):
    # def __init__(self, loop, logbuffer):
    #     self._buttons = HSplit(
    #         [Button("command_2", handler=self.command_2)],
    #         key_bindings=self.get_key_bindings(),
    #         modal=True,
    #     )
    #
    #     self.loop = loop
    #     self.logbuffer = logbuffer

    @property
    def buttons(self):
        return [Button("activate", handler=self.activate)]

    def activate(self):
        self.print("activate")


def main():
    use_asyncio_event_loop()
    loop = asyncio.get_event_loop()
    main_menu = MainMenu(loop)

    loop.run_until_complete(main_menu.app.run_async().to_asyncio_future())


if __name__ == "__main__":
    main()
