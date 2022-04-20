#include <iostream>
using namespace std;

class Complex
{
private:
	double real;
	double img;
public:
	Complex() :real(0), img(0) {}
	Complex(double real_, double img_) :real(real_), img(img_) {}
	Complex(const Complex& C) : real(C.real), img(C.img) {}
	Complex& operator+=(const Complex& x) { real += x.real; img += x.img; return *this; }
	Complex& operator+=(double a) { real += a; return *this; }
	friend Complex operator+=(double a, Complex& x);
	Complex operator+(const Complex& x) { return Complex(real + x.real, img + x.img); }
	Complex operator+(double a) { return Complex(real + a, img); }
	friend Complex operator+(double a, Complex& x);
	Complex& operator= (double a) { real = a; return *this; };
	Complex& operator= (const Complex& x)
	{
		if (this == &x)
			return *this;
		real = x.real; img = x.img;
		return *this;
	}
	friend ostream& operator << (ostream& ostr, Complex& C);
};

Complex operator+=(double a, Complex& x)
{
	x.real += a;
	return x;
}

Complex operator+(double a, Complex& x)
{
	return Complex(a + x.real, x.img);
}

ostream& operator << (ostream& ostr, Complex& C)
{
	ostr << C.real << " " << C.img << endl;

	return ostr;
}

int main()
{
	double x = 3.0, y = 4.0;
	Complex C1(1.0, 2.0), C2(11.0, 12.0);
	Complex C3 = C1 + C2;
	Complex C4 = C1 + x;
	Complex C5 = y + C1;
	cout << "C1 = " << C1 << "C2 = " << C2 << "C3 = " << C3 << "C4 = " << C4 << "C5 = " << C5 << endl;
	C5 = C4 = C3 = C2 += C1 += x;
	cout << "C1 = " << C1 << "C2 = " << C2 << "C3 = " << C3 << "C4 = " << C4 << "C5 = " << C5 << endl;

	return 0;
}
/*
C1 = 1 2
C2 = 11 12
C3 = 12 14
C4 = 4 2
C5 = 5 2

C1 = 4 2
C2 = 15 14
C3 = 15 14
C4 = 15 14
C5 = 15 14

*/