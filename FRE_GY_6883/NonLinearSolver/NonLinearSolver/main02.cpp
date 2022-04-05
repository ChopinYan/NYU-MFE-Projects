#include <iostream>
#include <iomanip>
#include "Function02.h"
#include "NonlinearSolver02.h"
using namespace std;
using namespace fre;


int main()
{
    double Acc1 = 0.0001, LEnd1 = 0.0, REnd1 = 2.0, Tgt1 = 0.0, Guess1 = 1.0;
    double Acc2 = 0.0001, LEnd2 = 0.0, REnd2 = 4.0, Tgt2 = 0.0, Guess2 = 3.0;
    
    NonlinearSolver solver(Tgt1, LEnd1, REnd1, Acc1, Guess1);
    F1 f1;
    cout << "Root of F1 by Bisection: " << fixed << setprecision(4) << solver.SolveByBisect(&f1) << endl;
    cout << "Root of F1 by Newton-Raphson: " << fixed << setprecision(4) << solver.SolveByNR(&f1) << endl << endl;
    
    solver.UpdateSolver(Tgt2, LEnd2, REnd2, Acc2, Guess2);
    F2 f2(10.0);
    cout << "Root of F2 by Bisection: " << fixed << setprecision(4) << solver.SolveByBisect(&f2) << endl;
    cout << "Root of F2 by Newton-Raphson: " << fixed << setprecision(4) << solver.SolveByNR(&f2) << endl << endl;

    return 0;
}