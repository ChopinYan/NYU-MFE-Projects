#include "PathDepOption02.h"
#include <cmath>
namespace fre {
	double PathDepOption::PriceByMC(MCModel& Model, long N, double epsilon)
	{
		double H = 0.0;
		int d = (int)delta.size();
		Vector Heps(d);
		for (int k = 0; k < d; k++) Heps[k] = 0.0;
		SamplePath S(m);
		for (long i = 0; i < N; i++)
		{
			Model.GenerateSamplePath(T, m, S);
			H = (i * H + Payoff(S)) / (i + 1.0);
			for (int k = 0; k < d; k++)
			{
				Rescale(S, k, 1.0 + epsilon);
				Heps[k] = (i * Heps[k] + Payoff(S)) / (i + 1.0);
				Rescale(S, k, 1/(1.0 + epsilon));
			}	
		}
		for (int k = 0; k < d; k++)
		{
			delta[k] = std::exp(-Model.GetR() * T) * (Heps[k] - H) / (epsilon * Model.GetS0()[k]);
		}
		Price = std::exp(-Model.GetR() * T) * H;
		return Price;
	}
	double ArthmAsianCall::Payoff(const SamplePath& S) const
	{
		double Ave = 0.0;
		int d = S[0].size();
		Vector one(d);
		for (int i = 0; i < d; i++) one[i] = 1.0;
		// sum = sum + V[j] * W[j]
		// sum_d(ave_m) = ave_m(sum_d)
		for (int k = 0; k < m; k++) Ave = (k * Ave + (one ^ S[k])) / (k + 1.0);  
		if (Ave < K) return 0.0;
		return Ave - K;
	}
	void Rescale(SamplePath& S, int d, double x)
	{
		int m = (int)S.size();
		for (int j = 0; j < m; j++) S[j][d] = x * S[j][d];
	}
}