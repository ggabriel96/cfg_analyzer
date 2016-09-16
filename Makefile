all: main.o analyzer.o
	g++ main.o analyzer.o -o cfg -Wall -O2

main.o: main.cpp
	g++ -c main.cpp -o main.o -Wall -O2

analyzer.o: analyzer.h analyzer.cpp
	g++ -c analyzer.cpp -o analyzer.o -Wall -O2

clean:
	rm main.o analyzer.o cfg
