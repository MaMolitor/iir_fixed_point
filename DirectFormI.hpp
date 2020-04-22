/*******************************************************************************

This header file has been taken from:
"A Collection of Useful C++ Classes for Digital Signal Processing"
By Vinnie Falco 

Bernd Porr adapted it for Linux and turned it into a filter using
fixed point arithmetic.

--------------------------------------------------------------------------------

License: MIT License (http://www.opensource.org/licenses/mit-license.php)
Copyright (c) 2009 by Vinnie Falco
Copyright (C) 2013-2017, Bernd Porr, mail@berndporr.me.uk
Copyright (C) 2020 , Mario Molitor , mario_molitor@web.de

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

*******************************************************************************/
#include<cstdint>

#ifndef DIRECTFORMI_HPP_
#define DIRECTFORMI_HPP_
class DirectFormI
{
public:
	// constructor with the coefficients b0,b1,b2 for the FIR part
        // and a1,a2 for the IIR part. a0 is always one.
	// the coefficients have been scaled up by the factor
	// 2^q which need to scaled down by this factor after every
	// time step which is taken care of.
	DirectFormI(const int b0, const int b1, const int b2,
			const int a1, const int a2,
			const int q = 15)
	{
		// coefficients are scaled by factor 2^q
		q_scaling = q;
		// FIR coefficients
		c_b0 = b0;
		c_b1 = b1;
		c_b2 = b2;
		// IIR coefficients
		c_a1 = a1;
		c_a2 = a2;
		reset();
	}

	// convenience function which takes the a0 argument but ignores it!
	DirectFormI(const int b0, const int b1, const int b2,
			const int, const int a1, const int a2,
			const int q = 15)
	{
		// coefficients are scaled by factor 2^q
		q_scaling = q;
		// FIR coefficients
		c_b0 = b0;
		c_b1 = b1;
		c_b2 = b2;
		// IIR coefficients
		c_a1 = a1;
		c_a2 = a2;
		reset();
	}

	DirectFormI(const DirectFormI &my)
	{
	// delay line
		m_x2 = my.m_x2; // x[n-2]
		m_y2 = my.m_y2; // y[n-2]
		m_x1 = my.m_x1; // x[n-1]
		m_y1 = my.m_y1; // y[n-1]

	// coefficients
		c_b0 = my.c_b0;
		c_b1 = my.c_b1;
		c_b2 = my.c_b2; // FIR
		c_a1 = my.c_a1;
		c_a2 = my.c_a2; // IIR

	// scaling factor
		q_scaling = my.q_scaling; // 2^q_scaling
    }

	void reset ()
	{
		m_x1 = 0;
		m_x2 = 0;
		m_y1 = 0;
		m_y2 = 0;
	}

	// filtering operation: one sample in and one out
	inline int filter(const int in)
	{
		// calculate the output
		/* register */ int64_t out_upscaled = static_cast<int64_t>(c_b0) * static_cast<int64_t>(in)
			+ static_cast<int64_t>(c_b1) * static_cast<int64_t>(m_x1)
			+ static_cast<int64_t>(c_b2) * static_cast<int64_t>(m_x2)
			- static_cast<int64_t>(c_a1) * static_cast<int64_t>(m_y1)
			- static_cast<int64_t>(c_a2) * static_cast<int64_t>(m_y2);

		// scale it back from int to int
		int out = static_cast<int>(out_upscaled >> q_scaling);

		// update the delay lines
		m_x2 = m_x1;
		m_y2 = m_y1;
		m_x1 = in;
		m_y1 = out;

		return out;
	}

private:
	// delay line
	int m_x2; // x[n-2]
	int m_y2; // y[n-2]
	int m_x1; // x[n-1]
	int m_y1; // y[n-1]

	// coefficients
	int c_b0,c_b1,c_b2; // FIR
	int c_a1,c_a2; // IIR

	// scaling factor
	int q_scaling; // 2^q_scaling
};

#endif /* DIRECTFORMI_HPP_ */
