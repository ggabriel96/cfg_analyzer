#include "analyzer.h"
#include <string.h>
#include <iostream>
using namespace std;

ndfa at;
int cont = 256;
set<string> sep;
map<string, int> new_name;
map<int, string> old_name;

int read_grammar() {
  int start, cur, i;
  string line, name; bool brackets;
  while (getline(cin, line)) {
    prod p; brackets = false; line.append(" |");
    for (start = i = 0; line[i] != '\0'; i++) {
      if (line[i] == ' ') continue;
      if (line[i] == '|')
        {at[start].push_back(p); p.clear(); }
      else if (line[i] == '<' && i + 1 < (int) line.length() && line[i + 1] != '=' && line[i + 1] != ' ') brackets = true;
      else if (line[i] == '>' && brackets == true) {
        brackets = false;
        if (new_name.find(name) == new_name.end()) {
          old_name[cont] = name;
          new_name[name] = cont++;
        }
        cur = new_name[name]; name.clear();
        if (!start) { start = cur; while (line[++i] != '='); }
        else p.push_back(Symbol(cur, false));
      }
      else if (brackets) name.append(&line[i], 1);
      else p.push_back(Symbol((int) line[i], true));
    }
  }
  return 0;
}

void build_ndfa() {

}

void print_prod(prod p) {
  for (auto& k: p)
    if (k.isterm) printf("%c", k.name);
    else printf("<%s>", old_name[k.name].c_str());
  printf(" | ");
}

void print_ndfa() {
  for (auto& i : at) {
    printf("<%s> ::= ", old_name[i.first].c_str());
    for (auto& j: i.second) {
      print_prod(j);
    }
    printf("\n");
  }
}
