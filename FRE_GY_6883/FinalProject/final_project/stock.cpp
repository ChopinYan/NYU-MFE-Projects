// File name: stock.cpp
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment

#include "stock.h"
#include <iostream>
#include <iomanip>
#include <algorithm>
using namespace std;


void Stock::CalcReturns()
{
    stk_returns.push_back(0.0);
    bmk_returns.push_back(0.0);
    cum_returns.push_back(0.0);
    abn_returns.push_back(0.0);
    double stk_return;
    double bmk_return;
    double abn_return;
    double cum_return;
    cum_return=0.0;
    
    for (int i = 1; i < (int)stk_prices.size(); i++) {

        // stk_return = stk_prices[i] / stk_prices[i - 1] - 1;
        stk_return = log(stk_prices[i] / stk_prices[i - 1]);
        stk_returns.push_back(stk_return);

        // bmk_return = bmk_prices[i] / bmk_prices[i - 1] - 1;
        bmk_return = log(bmk_prices[i] / bmk_prices[i - 1]);
        bmk_returns.push_back(bmk_return);

        abn_return = stk_returns[i] - bmk_returns[i];
        abn_returns.push_back(abn_return);
        
        // direct cumulative sum of Daily return 
        cum_return = cum_return + stk_return;

        cum_returns.push_back(cum_return);
    }
}

void Stock::Display(int N)
{   string output_group_name;
    if (group_label == 1) {
        output_group_name= "Miss";
    }
    else if (group_label == 2) {
        output_group_name= "Meet";
    }
    else {
        output_group_name= "Beat";
    }

    cout << "Ticker: " << this->GetTicker() << endl;
    cout << "Group: " << output_group_name << endl;
    cout << "Announcment Date: " << this->GetAnnDate() << endl;
    cout << "Period End: " << this->GetEndDate() << endl;
    cout << "Estimate EPS: " << this->GetEstmEPS() << endl;
    cout << "Reported EPS: " << this->GetReptEPS() << endl;
    cout << "Surprise: " << this->GetSurprise() << endl;
    cout << "Surprise Percent: " << this->GetSurprisePct() << endl;
    cout << "Daily Prices, Daily Returns and Cumulative Daily Returns:" << endl << endl;
    cout << setw(15) << "Dates"
        << setw(15) << "Prices"
        << setw(15) << "Daily Returns"
        << setw(15) << "Cum Returns"
        << endl << endl;

  
    start_date_index = N - N;
    end_date_index = N + N;
    for (int i = start_date_index; i <= end_date_index; i++) {
        cout << setw(15) << date_range[i] 
            << setw(15) << stk_prices[i]
            << setw(15)<< stk_returns[i]
            << setw(15) << cum_returns[i] << endl;
        cout << endl;
    }
    cout << endl;
}
