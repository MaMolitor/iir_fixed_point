all: fixeddemo


fixeddemo: DirectFormI.hpp fixeddemo.cpp
	g++ -Ofast -o fixeddemo fixeddemo.cpp

clean:
	rm -f fixeddemo unfiltered.dat filtered.dat
