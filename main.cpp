#include <stdio.h>
#include "analyzer.h"
using namespace std;

int main(int argc, char const *argv[]) {
  read_grammar();
  print_ndfa();
  return 0;
}
