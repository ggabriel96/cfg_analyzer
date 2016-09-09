#include "analyzer.h"
#include <string.h>
#include <iostream>
using namespace std;

map<string, int> new_name;
map<int, string> old_name;
ndfa at;

int cont = 256;

int read_grammar() {
  string line, name; bool brackets; int start, i, cur;
  while (getline(cin, line)) {
    prod p; brackets = false; line.append("|");
    for (start = i = 0; line[i] != '\0'; i++) {
      if (line[i] == ' ') continue;
      if (line[i] == '|')
        { at[start].push_back(p); p.clear(); }
      else if (line[i] == '<') brackets = true;
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

void print_ndfa() {
  for (auto& i : at) {
    printf("%d ::= ", i.first);
    for (auto& j: i.second) {
      for (auto& k: j) printf(".%d", k.name);
      printf(" | ");
    }
    printf("\n");
  }
}
