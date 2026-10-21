"""The package diagram of Chapter 4 as a test: dependencies only point downwards.

    view <- controller -> service / ai -> dao -> model
A forbidden import fails the build the moment it is written (NFR09 maintainability).
"""
import ast
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORBIDDEN = {
    "model": {"dao", "service", "ai", "controller", "view", "shop"},
    "dao": {"service", "ai", "controller", "view", "shop"},
    "service": {"controller", "view", "shop", "ai"},
    "ai": {"controller", "view", "shop", "service"},
    "controller": {"dao", "shop"},
    "view": {"dao", "service", "ai", "shop", "controller"},
}


def imported_packages(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


def modules_of(layer):
    for folder, _, files in os.walk(os.path.join(ROOT, layer)):
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(folder, f)


@pytest.mark.parametrize("layer", FORBIDDEN)
def test_dependencies_only_point_downwards(layer):
    for module in modules_of(layer):
        illegal = imported_packages(module) & FORBIDDEN[layer]
        assert not illegal, f"{os.path.relpath(module, ROOT)} imports {illegal}"


def test_services_never_import_a_storage_implementation():
    for module in modules_of("service"):
        source = open(module, encoding="utf-8").read()
        assert "sqlite" not in source.lower(), module
