from pathlib import Path
from typing import List, Optional
from pprint import pprint

from clang.cindex import Cursor, CursorKind, Index, CompilationDatabase

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
    return list(filter(lambda child: child.kind == CursorKind.STRUCT_DECL or child.kind == CursorKind.CLASS_DECL, cursor.get_children()))

def main():
    prj_root = find_project_root()
    if prj_root is None:
        print("Can't find project root!")
        exit(1)
    print(prj_root)
    
    db = CompilationDatabase.fromDirectory(prj_root / 'build')
    for cc in db.getAllCompileCommands():
        pprint({ 'args': list( cc.arguments ), 'filename': cc.filename, 'dir': cc.directory })

    index = Index.create()
    # tu = index.parse(input('path: '))

    # TODO: Pass args from compilation db to index.parse
    tu = index.parse('src/test.cpp', ['-DBUZZY_BOI=1', '-I' + str(prj_root) + '/include'])
    cursor = tu.cursor
    classes = get_classes(cursor)
    print('Found classes or structs')
    print(list(map(lambda inc: inc.include, tu.get_includes())))
    for c in classes:
        print(f'{c.displayname} {c.type.get_size()} bytes')
        for child in c.get_children():
            print(f'   name={child.displayname}, type={child.type.spelling}, size={child.type.get_size()}, kind={child.kind}')

