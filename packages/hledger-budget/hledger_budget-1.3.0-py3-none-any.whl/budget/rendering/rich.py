from typing import Any

from budget.table import Table, Text
from budget.utils import rprint

from rich import box
from rich.table import Table as RichTable
from rich.text import Text as RichText

from ._renderer import Renderer


class RichRenderer(Renderer):
    def render_table(self, table: Table):
        kw: dict[str, Any] = {"box": box.MINIMAL_HEAVY_HEAD}

        if table.title:
            kw["title"] = table.title

        if any(table.header):
            kw["show_header"] = True
            kw["header_style"] = "bold"

        if table.footer:
            kw["show_footer"] = True

        rt = RichTable(**kw)
        messages: set[tuple[int, str]] = set()
        for i, header in enumerate(table.header):
            footer = to_rich_text(table.footer[i]) if table.footer else ""
            colstyle = table.styles[i]
            rt.add_column(to_rich_text(header), footer, justify=colstyle.justify)

        for row in table.rows:
            textrow = []
            for cell in row:
                textrow.append(to_rich_text(cell))
                msg = cell.metadata.get("message")
                if msg:
                    messages.add((len(messages), msg))

            rt.add_row(*textrow)

        rprint(rt)

        if messages:
            # Use grid for pretty-printing of wrapped lines after the dash.
            # Yay, what a hack! :)
            grid = RichTable.grid(padding=(0, 1))
            grid.add_column()
            grid.add_column(style="alt")
            for _, desc in sorted(messages):
                grid.add_row("-", desc)

            rprint(grid)


def to_rich_text(other: Text):
    return RichText(other.get_text(sep="\n"), style=other.style)
