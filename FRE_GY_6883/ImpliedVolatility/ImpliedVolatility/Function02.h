#pragma once
namespace fre {
	class Function
	{
	public:
		virtual double Value(double x) = 0;
		virtual double Deriv(double x) = 0;
		virtual ~Function() {};
	};
}
