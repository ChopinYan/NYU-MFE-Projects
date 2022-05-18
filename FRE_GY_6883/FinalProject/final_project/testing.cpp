// File name: testing.cpp
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment

#include <iostream>
#include <map>
#include "stock.h"
#include "ProcessAnnoucement.h"
#include "libcurl.h"
#include "bootstrap.h"
#include "gnuplot.h"
#include "testing.h"
using namespace std;

map<string, Stock*> initialize_with_data_test(int& num, Stock* benchmark) {
    map<string, Stock*> stks = excel_reader(EOD_FILE);
    map<string, double> benchmark_map = fetch_benchmark_price(benchmark);
    vector<string> valid_dates;
    for (map<string, double>::iterator itr = benchmark_map.begin(); itr != benchmark_map.end(); itr++) {
        valid_dates.push_back(itr->first);
    }
    multithread_handler(stks, benchmark_map, valid_dates, num);
    return stks;
}

int run_tests() {
    int fail_num = 0;
    // Initialization
    map<string, double> benchmark_map;
    Bootstrap bts;
    string soption;
    string snumber;
    bool cont = true;
    string ticker;
    string sgroup;
    vector<double> X;
    int res = 0;

    // create empty stock object via default constructor
    Stock stk1;
    if ((!stk1.GetTicker().empty())) {
        cout << "(1) Failed to create empty Stock object with empty ticker name" << endl;
        res = -1;
    }

    // create Stock IWV via alternative constructor
    Stock* stk2 = new Stock("IWV"); // this is a dynamic allocation
    if (stk2->GetTicker() != "IWV") {
        cout << "(2) Failed to create Stock object with a given ticker name" << endl;
        res = -1;
    }
    delete stk2;
    stk2 = NULL;

    // create map of stocks based on the given excel file
    map<string, Stock*> stks = excel_reader(EOD_FILE);
    if (stks.size() != 2276) {  
        cout << "(3) Your EOD file is incomplete." << endl;
        res = -1;
    }

     //check whether there is a stock less than 2N+1: let N=90(max)
    Stock* benchmark_t4 = new Stock("IWV");
    int N = 90;
    map<string, Stock*>* stks_test = new map<string, Stock*>;
    *stks_test = initialize_with_data_test(N, benchmark_t4);
    for (auto itr_t4 = stks_test->begin(); itr_t4 != stks_test->end(); itr_t4++) {
        int length_t4 = (int)itr_t4->second->GetStkPrices().size();
        if (length_t4 < 2 * 90 + 1) {
            cout << "(4) Failed to delete the stock without enough historical prices for 2N+1." << endl;
            res = -1;
            break;
        }
    }
    delete benchmark_t4;
    benchmark_t4 = NULL;


    // check GroupDevider, the stocks in a group should be 1/3 of the size (some groups may have one more ticker than others) 
    map<string, Stock*>* stks_t5 = new map<string, Stock*>;
    *stks_t5 = excel_reader(EOD_FILE);
    vector<vector<string>>* grouplists_ptr = new vector<vector<string>>;
    *grouplists_ptr = GroupDivider(*stks_t5);
    for (int i = 0; i < 3; i++)
    {
        if (grouplists_ptr->at(i).size() != int(stks_t5->size() / 3) && grouplists_ptr->at(i).size() != int(stks_t5->size() / 3) + 1)
        {
            cout << "(5) Failed to devide groups." << endl;
            res = -1;
            break;
        }
    }
    delete stks_t5;
    delete grouplists_ptr;
    stks_t5 = NULL;
    grouplists_ptr = NULL;

    
    // check whether the return of the first day is 0
    Stock* benchmark_t6 = new Stock("IWV");
    for (auto itr_t6 = stks_test->begin(); itr_t6 != stks_test->end(); itr_t6++)
    {
        vector<double> returns = stks_test->begin()->second->GetStkReturns();
        if (returns[0] != 0.0)
        {
            cout << "(6) Failed to calculate daily returns." << endl;
            res = -1;
            break;
        }
    }
    delete benchmark_t6;
    benchmark_t6 = NULL;


    // check Bootstrap AAR_avg
    Stock* benchmark_t7 = new Stock("IWV");
    Bootstrap* bts_t7 = new Bootstrap;
    bts_t7->CalculationByBootstrapping(*stks_test);
    Matrix AAR_avg_t7 = bts_t7->GetAvgAAR();
    for (int i = 0; i < 3; i++)
    {
        if(AAR_avg_t7[i].size()!=2*N+1)  // check AAR-avg size
        {
            cout << "(7) Failed to calculate AAR_avg in Bootstrap." << endl;
            res = -1;
            break;
        }
        if(AAR_avg_t7[i][0] != 0.0)  // check AAR-avg of the first day is 0
        {
            cout << "(7) Failed to calculate AAR_avg in Bootstrap." << endl;
            res = -1;
            break;
        }
        for (int t = 1; t < 2 * N + 1; t++)  // check daily AAR_avg is in the range of [-1,1]
        {
            if (AAR_avg_t7[i][t] < -1.0 || AAR_avg_t7[i][t] > 1.0)
            {
                cout << "(7) Failed to calculate AAR_avg in Bootstrap." << endl;
                res = -1;
                break;
            }
        }
    }
    delete benchmark_t7;
    delete bts_t7;
    benchmark_t7 = NULL;
    bts_t7 = NULL;

    // check Bootstrap AAR_std
    Stock* benchmark_t8 = new Stock("IWV");
    Bootstrap* bts_t8 = new Bootstrap;
    bts_t8->CalculationByBootstrapping(*stks_test);
    Matrix AAR_std_t8 = bts_t8->GetAARstd();
    for (int i = 0; i < 3; i++)
    {
        if (AAR_std_t8[i].size() != 2 * N + 1)  // check AAR-std size
        {
            cout << "(8) Failed to calculate AAR_std in Bootstrap." << endl;
            res = -1;
            break;
        }
        if (AAR_std_t8[i][0] != 0.0)  //check AAR-std of the first day is 0
        {
            cout << "(8) Failed to calculate AAR_std in Bootstrap." << endl;
            res = -1;
            break;
        }
        for (int t = 1; t < 2 * N + 1; t++)  //check daily AAR_std is in the range of [0,1]
        {
            if (AAR_std_t8[i][t] <0.0 || AAR_std_t8[i][t] > 1.0)
            {
                cout << "(8) Failed to calculate AAR_std in Bootstrap." << endl;
                res = -1;
                break;
            }
        }
    }
    delete benchmark_t8;
    delete bts_t8;
    benchmark_t8 = NULL;
    bts_t8 = NULL;

    delete stks_test;
    stks_test = NULL;

    return res;
};