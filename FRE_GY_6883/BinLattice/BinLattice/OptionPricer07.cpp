#include <iostream>
#include <iomanip>
#include "BinomialTreeModel02.h"
#include "Option07.h"
using namespace std;
using namespace fre;


int main()
{
    int N = 8;
    double U = 1.15125, D = 0.86862, R = 1.00545;
    double S0 = 106.00, K = 100.00;
    BinomialTreeModel Model(S0, U, D, R);
    
    Call call(N, K);
    OptionCalculation callCalculation(&call);
    cout << "European Call Option Price = "
        << fixed << setprecision(2) << callCalculation.PriceByCRR(Model) << endl;
    
    Put put(N, K);
    OptionCalculation putCalculation(&put);
    cout << "European Put Option Price = "
        << fixed << setprecision(2) << putCalculation.PriceByCRR(Model) << endl;

    BinLattice CallPriceTree(N);
    cout << "American Call Option Price = "
        << fixed << setprecision(2) << callCalculation.PriceBySnell(Model, CallPriceTree) << endl;
    cout << "American Call Price Tree: " << endl << endl;
    CallPriceTree.Display();

    BinLattice PutPriceTree(N);
    cout << "American Put Option Price = "
        << fixed << setprecision(2) << putCalculation.PriceBySnell(Model, PutPriceTree) << endl;
    cout << "American Put Price Tree: " << endl << endl;
    PutPriceTree.Display();

    return 0;
}

// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
