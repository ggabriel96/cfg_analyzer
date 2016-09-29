all: main.o analyzer.o
	g++ main.o analyzer.o -o cfg -Wall -O2 -std=c++11

main.o: main.cpp
	g++ -c main.cpp -o main.o -Wall -O2 -std=c++11

analyzer.o: analyzer.h analyzer.cpp
	g++ -c analyzer.cpp -o analyzer.o -Wall -O2 -std=c++11

clean:
	rm main.o analyzer.o cfg
