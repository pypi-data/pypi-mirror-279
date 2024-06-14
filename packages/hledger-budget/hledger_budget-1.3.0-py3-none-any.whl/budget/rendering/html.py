from jinja2 import Environment, PackageLoader, select_autoescape

from budget.table import Table

from ._renderer import Renderer


class HTMLRenderer(Renderer):
    def __init__(self, bare: bool):
        self.bare = bare
        self.env = Environment(
            loader=PackageLoader("budget.rendering", "templates"),
            autoescape=select_autoescape(),
        )

    def render_table(self, table: Table):
        # https://jinja.palletsprojects.com/en/3.1.x/templates/#template-objects
        if self.bare:
            layout = self.env.get_template("table.html")
            template = None
        else:
            layout = self.env.get_template("page.html")
            template = self.env.get_template("table.html")

        print(layout.render(table=table, template=template))
