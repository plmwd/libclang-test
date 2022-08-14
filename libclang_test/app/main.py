from pathlib import Path
from typing import List, Optional

from clang.cindex import Cursor, CursorKind, Index

def dir_contains(dir: Path, patterns: List[str | Path]) -> bool:
    for pat in patterns:
        if Path(dir / pat).exists():
            return True
    return False

def find_project_root(patterns: Optional[List[str | Path]]=None) -> Optional[Path]:
    if patterns is None:
        patterns = ['.git']
    
    cwd = Path.cwd()
    while not dir_contains(cwd, patterns):
        if cwd == '/':
            return None
        cwd = cwd.parent

    return cwd

def traverse(node, depth=0):
    print(f'{"  " * depth} displayname={node.displayname}, kind={node.kind}, type={node.type.spelling}')
    for child in node.get_children():
        traverse(child, depth + 1)

def get_classes(cursor: Cursor) -> List[Cursor]:
    classes = []

    for child in cursor.get_children():
        if child.kind == CursorKind.STRUCT_DECL or child.kind == CursorKind.CLASS_DECL:
            classes.append(child)

    return classes

def main():
    prj_root = find_project_root()
    print(prj_root)

    index = Index.create()
    tu = index.parse('src/test.cpp')
    hu = index.parse('src/test.h')
    cursor = tu.cursor
    classes = get_classes(cursor)
    print('Found classes or structs')
    print(list(tu.get_includes()))
    for c in classes:
        print(f'{c.displayname} {c.type.get_size()} bytes')
        for child in c.get_children():
            print(f'   name={child.displayname}, type={child.type.spelling}, size={child.type.get_size()}, kind={child.kind}')

