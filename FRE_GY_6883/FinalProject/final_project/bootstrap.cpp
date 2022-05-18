// File name: bootstrap.cpp
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment

#include "bootstrap.h"
#include <iostream>
#include <iomanip>
#include <cmath>
#include <random>
using namespace std;

vector<vector<string>> GroupDivider(map<string, Stock*> &stocks)
{
    vector<vector<string>> grouped_stocks(3);
    for(map<string, Stock*>::iterator itr=stocks.begin(); itr!=stocks.end(); itr++)
    {
        if (itr->second->GetGroupLabel() == 1) grouped_stocks[0].push_back(itr->second->GetTicker());
        else if (itr->second->GetGroupLabel() == 2) grouped_stocks[1].push_back(itr->second->GetTicker());
        else grouped_stocks[2].push_back(itr->second->GetTicker());
    }
    return grouped_stocks;
}

vector<Vector> Bootstrap::SampledAAR(map<string, Stock*>& stocks, vector<vector<string>> grouped_stocks)
{
    vector<Vector> AAR(3);
    vector<map<int, bool>> JudgeMap(3);
    for (int i = 0; i < 3; i++)
    {
        
        AAR[i].resize(T,0.0);
        for (int j = 0; j < SampleNum; j++)
        {
            int RandIdx = rand() % grouped_stocks[i].size();
            if (!JudgeMap[i][RandIdx])
            {
                JudgeMap[i][RandIdx] = true;
                string ticker_j = grouped_stocks[i][RandIdx];
                Vector AR_j = stocks[ticker_j]->GetAbnReturns();
                AAR[i] = (1/(j + 1.0)) * (j * AAR[i] + AR_j);
            }
            else j--;
        } 
    }
    return AAR;
}

vector<Vector> Bootstrap::SampledCAAR(vector<Vector>& sampledAAR)
{
    vector<Vector> CAAR(3);
    for (int i = 0; i < 3; i++)
    {
        CAAR[i].resize(T);
        CAAR[i][0] = sampledAAR[i][0];
        for(int t = 1; t < T; t++)
        { 
            CAAR[i][t] = CAAR[i][t - 1] + sampledAAR[i][t];
        }
    }
    return CAAR;
}

void Bootstrap::CalculationByBootstrapping(map<string, Stock*>& stocks)
{
    T = (int)stocks.begin()->second->GetStkPrices().size();
    vector<vector<string>> grouped_stocks = GroupDivider(stocks);
    AAR_avg.clear();
    CAAR_avg.clear();
    AAR_std.clear();
    CAAR_std.clear();
    AAR_avg.resize(3, Vector(T, 0.0));
    CAAR_avg.resize(3, Vector(T, 0.0));
    AAR_std.resize(3, Vector(T, 0.0));
    CAAR_std.resize(3, Vector(T, 0.0));

    Matrix AARsq(3, Vector(T, 0.0));
    Matrix CAARsq(3, Vector(T, 0.0));
    
    srand((unsigned)time(NULL));
    for (int j = 0; j < RepeatTime; j++)
    {
        Matrix sampledAAR = SampledAAR(stocks, grouped_stocks);
        AAR_avg = (1.0 / (j + 1.0)) * (j * AAR_avg + sampledAAR); 
        AARsq = (1.0 / (j + 1.0)) * (j * AARsq + (sampledAAR ^ 2.0));
        Matrix sampledCAAR = SampledCAAR(sampledAAR);
        CAAR_avg = (1.0 / (j + 1.0)) * (j * CAAR_avg + sampledCAAR);
        CAARsq = (1.0 / (j + 1.0)) * (j * CAARsq + (sampledCAAR ^ 2.0));
    }
    AAR_std = (AARsq + (-1) * (AAR_avg^2.0))^0.5;  //Var = E(X^2) - (EX)^2; STD = Var^0.5 
    CAAR_std = (CAARsq + (-1) * (CAAR_avg ^ 2.0))^0.5;
}

void Bootstrap::Display(int groupnum)
{
    string groupname;
    if (groupnum == 0) { groupname = "MISS"; }
    else if(groupnum == 1) { groupname = "MEET"; }
    else { groupname = "BEAT"; }
    cout << "Detailed Information for " << groupnum << " Group:" << endl << endl;
    cout << setw(5) << "t"
        << setw(14) << "Avg AAR"
        << setw(14) << "AAR-STD"
        << setw(14) << "Avg CAAR"
        << setw(14) << "CAAR-STD"
        << endl << endl;
    for (int i = 0; i < T; i++) {
        cout << setw(5) << i-int(T/2)
            << setw(14) << AAR_avg[groupnum][i]
            << setw(14) << AAR_std[groupnum][i]
            << setw(14) << CAAR_avg[groupnum][i]
            << setw(14) << CAAR_std[groupnum][i]
            << endl << endl;
    }
}


