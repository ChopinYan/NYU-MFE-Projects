#pragma once
#include "Function01.h"
namespace fre {
	class NonlinearSolver
	{
	private:
		double Tgt, LEnd, REnd, Acc, Guess;
	public:
		NonlinearSolver(): Tgt(0), LEnd(0), REnd(0), Acc(0), Guess(0) {}
		NonlinearSolver(double Tgt_, double LEnd_, double REnd_, double Acc_, double Guess_): 
			Tgt(Tgt_), LEnd(LEnd_), REnd(REnd_), Acc(Acc_), Guess(Guess_) {}
		~NonlinearSolver() {}
		void UpdateSolver(double Tgt_, double LEnd_, double REnd_, double Acc_, double Guess_)
		{
			Tgt = Tgt_;
			LEnd = LEnd_;
			REnd = REnd_;
			Acc = Acc_;
			Guess = Guess_;
		}
		double SolveByBisect(double (*Fct)(double x));
		double SolveByNR(double (*Fct)(double x), double (*DFct)(double x));
	};
}