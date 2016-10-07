#include "analyzer.h"
#include <string.h>
#include <iostream>
#include <vector>
#include <array>
#include <map>
#include <set>
using namespace std;

ndfa at;
int cont = 256, conttokens;
set<string> sep;
// vetor de inteiros indicando os estados especiais que precisamos seguir
// as produções para montarmos um token, como variáveis, números, strings...
// esses estados estão marcados com '*' no primeiro caractere da linha
set<string> separators;
set<int> special, finals;
map<string, int> new_name;
map<int, string> old_name;
vector< array<vector<int>, 256> > ndfatok;

void init() {
  separators.insert(" ");
  separators.insert("(");
  separators.insert(")");
  separators.insert("+");
  separators.insert("-");
  separators.insert("*");
  separators.insert("/");
  separators.insert("%");
  separators.insert("^");
  separators.insert("?");
  separators.insert(":");
  separators.insert("<");
  separators.insert("=");
  separators.insert(">");
  separators.insert("[");
  separators.insert("]");
  separators.insert("{");
  separators.insert("}");
  separators.insert(".");
  separators.insert(",");
  separators.insert(";");
  separators.insert("'"); // ?
  separators.insert("\""); // ?
  // separators.insert("or");
  // separators.insert("and");
  // separators.insert("not");
  // separators.insert("<=");
  // separators.insert("==");
  // separators.insert(">=");
}

int read_grammar() {
  string line, name;
  int start = 0, cur = 0, i = 0;
  bool marked, brackets, quotes;
  while (getline(cin, line)) {
    prod p;
    line.append(" |");
    marked = brackets = quotes = false;
    for (i = 0; line[i] != '<' && line[i] != '\0'; i++)
      if (line[i] == '*')
        { line[i] = ' '; marked = true; break; }
    for (start = i = 0; line[i] != '\0'; i++) {
      if (quotes) {

      } else {
        if (line[i] == '"') quotes = true;
      }
      if (line[i] == ' ') continue;
      if (line[i] == '|')
        { at[start].push_back(p); p.clear(); }
      else if (line[i] == '<') brackets = true;
      else if (line[i] == '>' && brackets == true) {
        brackets = false;
        if (new_name.find(name) == new_name.end()) {
          printf("%d: %s\n", cont, name.c_str());
          old_name[cont] = name;
          new_name[name] = cont++;
        }
        cur = new_name[name]; name.clear();
        if (marked) { special.insert(cur); marked = false; }
        if (!start) { start = cur; while (line[++i] != '='); }
        else p.push_back(Symbol(cur, false));
      }
      else if (line[i] == '"')
      else if (brackets) name.append(&line[i], 1);
      else p.push_back(Symbol((int) line[i], true));
    }
  }
  printf("\nSpecial states:\n");
  for (auto& s: special) {
    printf("%d\n", s);
  }
  return 0;
}

// vector< array<vector<int>, 256> > ndfatok;
void build_ndfa() {
  unsigned int state_from = 0;
  // ndfatok.push_back(array<vector<int>, 256>());
  for (auto& rule: at) {
    printf("Rule %d\n", rule.first);
    if (special.find(rule.first) != special.end()) {
      // Especial, trata diferente, bjs
      continue;
    }
    for (auto& prod: rule.second) {
      state_from = 0;
      for (auto& sym: prod) {
        printf("state_from: %d, sym: '%c', %sterm\n", state_from, (char) sym.name, sym.isterm ? "" : "!");
        if ((char) sym.name == '&') continue;
        if (sym.isterm) {
          if (ndfatok.size() <= state_from) {
            ndfatok.push_back(array<vector<int>, 256>());
          }
          ndfatok[state_from][sym.name].push_back(ndfatok.size());
          state_from = ndfatok.size();
        }
        // tokens de mais de um char estão indo para outros estados, ao invés de ficar naquele que eles têm que reconhecer, como o 'or' e 'and'. Além disso, '<=' está sendo quebrado em dois tokens porque '<' e '=' são separadores
        if (is_separator(sym) || !sym.isterm) {
          if (state_from == 0) continue;
          printf("State %d is final, sep '%c'\n\n", state_from, (char) sym.name);
          finals.insert(state_from);
          state_from = 0;
        }
      }
      if (state_from > 0) {
        printf("State %d is final, end of prod\n\n", state_from);
        finals.insert(state_from);
      }
    }
  }
  print_finals();
}

bool is_separator(symbol_t &sym) {
  return separators.find(string((char *) &sym.name)) != separators.end();
}

void print_finals() {
  printf("\nprint_finals:\n");
  for (auto& f: finals)
    printf("{%d}\n", f);
}

void print_prod(prod p) {
  for (auto& k: p)
    if (k.isterm) printf("%c", k.name);
    else printf("<%s>", old_name[k.name].c_str());
  printf(" | ");
}

void print_ndfa() {
  printf("\nprint_ndfa:\n");
  for (auto& i : at) {
    printf("<%s> ::= ", old_name[i.first].c_str());
    for (auto& j: i.second) {
      print_prod(j);
    }
    printf("\n");
  }
}


// vector< array<vector<int>, 256> > ndfatok;
void print_ndfatokens() {
  unsigned i, j, size = ndfatok.size();
  for (i = 0; i < size; i++) {
    auto& state_from = ndfatok[i];
    printf("\nFrom state %d\n", i);
    for (j = 0; j < 256; j++) {
      auto& state_to = state_from[j];
      if (state_to.empty()) continue;
      printf("through %c: ", (char) j);
      for (auto& state: state_to)
        if (state != 0) printf("[%d]", state);
      printf("\n");
    }
    printf("\n");
  }
}
