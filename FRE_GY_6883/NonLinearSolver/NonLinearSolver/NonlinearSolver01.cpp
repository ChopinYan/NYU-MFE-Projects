#include "Function01.h"
#include "NonlinearSolver01.h"
#include <cmath>
namespace fre {
	double NonlinearSolver::SolveByBisect(double (*Fct)(double x))
	{
		double left = LEnd, right = REnd, mid = (left + right) / 2;
		double y_left = Fct(left) - Tgt, y_mid = Fct(mid) - Tgt;
		
		while (mid - left > Acc)
		{
			if ((y_left * y_mid) > 0)
			{
				left = mid; y_left = y_mid;
			}
			else right = mid;
			mid = (left + right) / 2;
			y_mid = Fct(mid) - Tgt;
		}

		return mid;
	}

	double NonlinearSolver::SolveByNR(double (*Fct)(double x), double (*DFct)(double x))
	{
		double x_prev = Guess;
		double x_next = x_prev - (Fct(x_prev) - Tgt) / DFct(x_prev);
		
		while (abs(x_next - x_prev) > Acc)
		{
			x_prev = x_next;
			x_next = x_prev - (Fct(x_prev) - Tgt) / DFct(x_prev);
		}
		return x_next;
	}
}