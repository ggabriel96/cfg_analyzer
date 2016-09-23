#include <stdio.h>
#include "analyzer.h"
using namespace std;

int main(int argc, char const *argv[]) {
  init();
  read_grammar();
  print_ndfa();
  build_ndfa();
  return 0;
}
