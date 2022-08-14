from pathlib import Path
from typing import List, Optional
from clang.cindex import Index

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

def main():
    prj_root = find_project_root()
    print(prj_root)

    index = Index.create()
    tu = index.parse('src/test.cpp')
    cursor = tu.cursor
    traverse(cursor)
