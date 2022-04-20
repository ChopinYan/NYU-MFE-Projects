// BasketOptions.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include "PathDepOption02.h"
#include "Matrix.h"
using namespace std;
using namespace fre;
int main()
{
    int d = 3;
    Vector S0(d);
    S0[0] = 40.0;
    S0[1] = 60.0;
    S0[2] = 100.0;
    double r = 0.03;
    double epsilon = 0.001;
    Matrix C(d);  // d Vectors inside
    for (int i = 0; i < d; i++) C[i].resize(d);  // every Vector inside C is of size d
    C[0][0] = 0.1; C[0][1] = -0.1; C[0][2] = 0.0;
    C[1][0] = -0.1; C[1][1] = 0.2; C[2][2] = 0.0;
    C[2][0] = 0.0; C[2][1] = 0.0; C[2][2] = 0.3;
    MCModel Model(S0, r, C);
    double T = 1.0 / 12.0, K = 200.0;
    int m = 30;
    Vector delta(d);
    ArthmAsianCall Option(T, K, m, delta);
    long N = 3000;
    cout << "Arithmetic Basket Call Price = " << Option.PriceByMC(Model, N, epsilon) << endl;
    Vector Delta = Option.GetDelta();
    cout << "Delta of Arithmetic Basket Call= " << Delta << endl;
    return 0;
}

/*
Arithmetic Basket Call Price = 2.18643
Delta of Arithmetic Basket Call= 0.506472 0.514193 0.530379
*/
