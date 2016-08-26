#include <map>
#include <string>
#include <vector>
using namespace std;

typedef struct Token {
  string name;
  boolean isterm;
} token_t;

typedef vector< token_t > prod;
typedef map< string, vector<prod> > ndfa;
