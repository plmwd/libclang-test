#include "test.h"
#include "some.hpp"
#include <cstdio>
#include <stdio.h>

class Bar {
public:
  Foo f1;
  Foo f2;
#ifdef BUZZY_BOI
  Bazz f;
#endif
  int bb;
};

int main(int argc, char *argv[]) {
  printf("hello world!\n");
  return 0;
}
