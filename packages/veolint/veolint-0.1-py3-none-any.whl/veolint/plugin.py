from flake8_plugin_utils import Plugin, Visitor, Error


class NoEmptyLineAfterClassDef(Error):
    code = 'C901'
    message = 'C999 no empty line after class definition without docstring'


class NoEmptyLineAfterClassDefVisitor(Visitor):
    def visit_ClassDef(self, node):
        if not node.body:
            return

        first_node = node.body[0]
        if not hasattr(first_node, 'lineno'):
            return

        if first_node.lineno - node.lineno == 2:
            self.error_from_node(NoEmptyLineAfterClassDef, node)


class Veolint(Plugin):
    name = 'flake8_custom_plugin'
    version = '0.1'
    visitors = [NoEmptyLineAfterClassDefVisitor]


if __name__ == '__main__':
    from flake8.main import application
    app = application.Application()
    app.run()
