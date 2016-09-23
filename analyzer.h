#include <map>
#include <string>
#include <vector>
using namespace std;

struct Symbol {
  int name;
  bool isterm;
  Symbol() {}; Symbol(int _n, bool _t) : name(_n), isterm(_t) {};
};

typedef vector< Symbol > prod;
typedef map< int, vector<prod> > ndfa;

void init();
int read_grammar();
void build_ndfa();
void print_prod(prod);
void print_ndfa();
