# -*-coding:utf8;-*-
import ast


class ClassParser(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node.body = self._transform_body(node.body)
        self.generic_visit(node)
        return node

    def visit_If(self, node):
        node.body = self._transform_body(node.body)
        if node.orelse:
            node.orelse = self._transform_body(node.orelse)
        self.generic_visit(node)
        return node

    def visit_While(self, node):
        node.body = self._transform_body(node.body)
        self.generic_visit(node)
        return node

    def visit_For(self, node):
        node.body = self._transform_body(node.body)
        self.generic_visit(node)
        return node

    def _transform_body(self, body):
        new_body = []
        for stmt in body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                if stmt.value.value == "end":
                    continue
            new_body.append(stmt)
        return new_body
