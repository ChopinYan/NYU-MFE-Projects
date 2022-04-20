#pragma once
#include <vector>
#include <cstdlib>  // srand and rand
#include <ctime>  // time
using namespace std;
namespace fre {
	typedef vector<double> SamplePath;  // 为复杂的声明定义一个新的简单的别名
	class MCModel
	{
	private:
		double S0, r, sigma;
	public:
		MCModel() : S0(0.0), r(0.0), sigma(0.0) {}
		MCModel(double S0_, double r_, double sigma_) : S0(S0_), r(r_), sigma(sigma_)
		{
			srand((unsigned)time(NULL));  // srand((unsigned)1)
		}
		void GenerateSamplePath(double T, int m, SamplePath& S) const;
		double GetS0() const { return S0; }
		double GetR() const { return r; }
		double GetSigma() const { return sigma; }
		void SetS0(double S0_) { S0 = S0_; }
		void SetR(double r_) { r = r_; }
		void SetSigma(double sigma_) { sigma = sigma_; }
	};
}
