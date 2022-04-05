#include <iostream>
#include <iomanip>
#include "BinomialTreeModel02.h"
#include "Option08.h"
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

    BinLattice<double> CallPriceTree(N);
    BinLattice<bool> CallStoppingTree(N);
    cout << "American Call Option Price = "
        << fixed << setprecision(2) << 
        callCalculation.PriceBySnell(Model, CallPriceTree, CallStoppingTree) << endl;
    cout << "American Call Price Tree: " << endl << endl;
    CallPriceTree.Display();
    cout << "American Call Exercise Policy: " << endl << endl;
    CallStoppingTree.Display();

    BinLattice<double> PutPriceTree(N);
    BinLattice<bool> PutStoppingTree(N);
    cout << "American Put Option Price = "
        << fixed << setprecision(2) << 
        putCalculation.PriceBySnell(Model, PutPriceTree, PutStoppingTree) << endl;
    cout << "American Put Price Tree: " << endl << endl;
    PutPriceTree.Display();
    cout << "American Put Exercise Policy: " << endl << endl;
    PutStoppingTree.Display();

    return 0;
}
