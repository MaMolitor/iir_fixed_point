//============================================================================
// Name        : fixeddemo.cpp
// Author      : Mario Molitor
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================
// Simulates a realtime system by sending a 12 bit integer ECG
// through a 50Hz fixed point IIR bandstop

// standard I/O stuff
#include <stdio.h>
#include <assert.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <list>
#include <iterator>

// includes the 2nd order IIR filter
#include "DirectFormI.hpp"

// Notch filter, 2nd order bandstop which means 2 biquad filters
// 50Hz notch frequency, sampling rate 1kHz
//
// generated by the Python script gen_coeff with q=14
// [ 15672. -29825.  15672.  16384. -30222.  15624.]
// [ 16384. -31180.  16384.  16384. -30753.  15720.]

// We loop through the ECG file with the 50Hz contamination
// and save a file which has the 50Hz removed!
int main (int,char**)
{
	// generated by the script 'gen_coeff.py' and then
	// copy/pasted in the filter


	std::list<DirectFormI> listofBiquads;
	std::ifstream coeff_file ("coeff.dat");
	 if (coeff_file.is_open())
	 {
		std::string line;
		while ( std::getline (coeff_file,line) )
		{
				char delim;
				short int b0 = 0,b1 = 0,b2 =0 ,a0 = 0,a1 = 1, a2 = 0, q = 0;
				std::istringstream iss(line.c_str());
				std::string temp;
				iss >> b0 >> delim >> b1 >> delim >> b2 >> delim >> a0 >> delim >> a1 >> delim >> a2 >> delim >> q;
				listofBiquads.push_back(DirectFormI(b0,b1,b2,a0,a1,a2,q));
		}
		coeff_file.close();
	  }

/*
	listofBiquads.push_back(DirectFormI(14511,-27615,14511,16384,-30157,15395,14));
	listofBiquads.push_back(DirectFormI(16384,-31180,16384,16384,-30362,15442,14));
	listofBiquads.push_back(DirectFormI(16384,-31180,16384,16384,-30222,15624,14));
	listofBiquads.push_back(DirectFormI(16384,-31180,16384,16384,-30753,15720,14));
	listofBiquads.push_back(DirectFormI(16384,-31180,16384,16384,-30572,16095,14));
	listofBiquads.push_back(DirectFormI(16384,-32768,16384,16384,-23009,12057,14));
*/

	FILE *finput = fopen("unfiltered.dat","rt");
	assert(finput != NULL);
	FILE *foutput = fopen("filtered.dat","wt");
	assert(foutput != NULL);

	for(;;)
	{
		// the data file has 3 channels and time
		short x1,x2,x3,y;
		int t;
		if (fscanf(finput,"%d %hd %hd %hd\n",&t,&x1,&x2,&x3)<1) break;
		y = x2;
		std::list<DirectFormI>::iterator it;

		// Make iterate point to begining and incerement it one by one till it reaches the end of list.
		for (it = listofBiquads.begin(); it != listofBiquads.end(); it++)
		{
			// Access the object through iterator
			y = it->filter(y);
		}

		fprintf(foutput,"%d %hd\n",t,y);
	}
	fclose(finput);
	fclose(foutput);
	fprintf(stderr,"Done!\n");
	return 0;
}
