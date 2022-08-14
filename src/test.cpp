#include <cstdio>
#include <stdio.h>

struct Foo {
  int a;
  int b;
  char c[10];
};

struct Bar {
  Foo f1;
  Foo f2;
  int bb;
};

int main(int argc, char *argv[]) {
  printf("hello world!\n");
  return 0;
}
