#include <iostream>
using namespace std;
class DefInt
{
protected:
    double a, b;
    int N;
    double (*f)(double x);
public:
    // DefInt(): a(0), b(0), N(0), f(0) {}
    // DefInt(DefInt& defInt) : a(defInt.a), b(defInt.b), N(defInt.N), f(defInt.f) {}
    DefInt(double a_, double b_, int N_, double (*f_)(double x))
        : a(a_), b(b_), N(N_), f(f_) {}  // problem
    // {
    //    a = a_; b = b_; N = N_; f = f_;
    // }
    virtual double Approximation() = 0;
    virtual ~DefInt() {}
};
class ByTrapezoid : public DefInt
{
public:
    // Complete the implementation of the constructor with parameters for class ByTrapezoid.
    // You are not allowed to create other member functions.
    ByTrapezoid(double a_, double b_, int N_, double (*f_)(double x)) : DefInt(a_, b_, N_, f_)
    {
    }
    double Approximation();
    ~ByTrapezoid() {}
};
double ByTrapezoid::Approximation()
{
    cout << "ByTrapezoid: ";
    double h = (b - a) / N;
    double Result = 0.5 * f(a);
    for (int n = 1; n < N; n++) Result += f(a + n * h);
    Result += 0.5 * f(b);
    return Result * h;
}
class BySimpson : public DefInt
{
public:
    // Complete the implementation of the constructor with parameters for class BySimpson.
    // You are not allowed to create other member functions.
    BySimpson(double a_, double b_, int N_, double (*f_)(double x)) : DefInt(a_, b_, N_, f_)
    {
    }
    double Approximation();
    ~BySimpson() {}
};
double BySimpson::Approximation()
{
    cout << "BySimpson: ";
    double h = (b - a) / N;
    double Result = f(a);
    for (int n = 1; n < N; n++) Result += 4 * f(a + n * h - 0.5 * h) + 2 * f(a + n * h);
    Result += 4 * f(b - 0.5 * h) + f(b);
    return Result * h / 6;
}
class Calculation
{
private:
    DefInt* ptr;
public:
    // Calculation(DefInt* ptr_): ptr(ptr_) {}
    void SetPtr(DefInt* ptr_)
    {
        ptr = ptr_;
    }
    double Appximation()
    {
        return ptr->Approximation();
    }
};
double f(double x) { return x * x * x - x * x + 1; }
int main()
{
    double a = 1.0;
    double b = 2.0;
    int N = 1000;
    DefInt* ptr1 = new ByTrapezoid(a, b, N, f); // (1) allocate memory for size(ByTrapzoid), (2) Call constructor for initialization
    DefInt* ptr2 = new BySimpson(a, b, N, f);
    // Calculation cal1(ptr1), cal2(ptr2);
    Calculation cal1, cal2;
    // Complete the missing codes in main function.
    // you must use cal1 and cal2 for your calculation.
    // You cannot use ptr1 or ptr2 directly for your calculation
    cal1.SetPtr(ptr1);
    cal2.SetPtr(ptr2);
    cout << cal1.Appximation() << endl;
    cout << cal2.Appximation() << endl;
    delete ptr1; // 1) destructor is invoked to destroy a, b, N and function pointer (2) free the allocated memory for sizeof(ByTrapziod)
    delete ptr2;
    ptr1 = NULL;
    ptr2 = NULL;
    return 0;
}


/*
ByTrapezoid: 0
BySimpson: 0
*/



/*
#include <iostream>
#include <iomanip>
using namespace std;
    
class DefInt
{
protected:
    double a, b;
    int N;
    double (*fct)(double x);
public:
    DefInt(double a_, double b_, int N_, double (*fct_)(double x)): 
        a(a_), b(a_), N(N_), fct(fct_) {}
    virtual double Approximation() = 0;
    virtual ~DefInt() {}  // =0
};

class ByTrapezoid : public DefInt
{
public:
    ByTrapezoid(double a_, double b_, int N_, double (*fct_)(double x)): 
        DefInt(a_, b_, N_, fct_) {}  // construct base class
    double Approximation();
    ~ByTrapezoid() {}
};
double ByTrapezoid::Approximation()
{
    double h = (b - a) / N;
    double result = 0.5 * fct(a);
    for (int k = 1; k < N; k++)
    {
        result += fct(a + k * h);
    }
    result += 0.5 * fct(b);
    return result * h;
}

class BySimpson : public DefInt
{
public:
    BySimpson(double a_, double b_, int N_, double (*fct_)(double x)) :
        DefInt(a_, b_, N_, fct_) {}
    double Approximation();
    ~BySimpson() {}
};
double BySimpson::Approximation()
{
    double h = (b - a) / N;
    double result = fct(a);
    for (int k = 1; k < N; k++)
    {
        result += 4 * fct(a + k * h - 0.5 * h) + 2 * fct(a + k * h);
    }
    result += 4 * fct(b - 0.5 * h) + fct(b);
    return result * h / 6;
}

class Calculation
{
private:
    DefInt* ptr;
public:
    // Calculation() {}
    // Calculation(DefInt* ptr_): ptr(ptr_) {}  //problem
    void SetPtr(DefInt* ptr_)
    {
        ptr = ptr_;
    }
    double Appximation()
    {
        return ptr->Approximation();
    }
};

double f(double x)
{
    return x * x * x - x * x + 1;
}

int main()
{
    double a = 1.0, b = 2.0;
    int N = 1000;
    DefInt* ptr1 = new ByTrapezoid(a, b, N, f);
    DefInt* ptr2 = new BySimpson(a, b, N, f);

    Calculation cal1;
    Calculation cal2;
    cal1.SetPtr(ptr1);
    cal2.SetPtr(ptr2);

    cout << "ByTrapezoid: " << fixed << setprecision(5) << cal1.Appximation() << endl;
    cout << "BySimpson: " << fixed << setprecision(5) << cal2.Appximation() << endl;

    delete ptr1;
    ptr1 = NULL;
    delete ptr2;
    ptr2 = NULL;

    return 0;
}
*/
