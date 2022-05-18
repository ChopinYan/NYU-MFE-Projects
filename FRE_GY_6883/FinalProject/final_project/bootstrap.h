// File name: bootstrap.h
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment

#pragma once
#include <stdio.h>
#include <string>
#include "stock.h"
#include "MatrixOperator.h"

using namespace std;

vector<vector<string>> GroupDivider(map<string, Stock*>& stocks);

class Bootstrap
{
private:
    int SampleNum = 80; // the number of samples in bootstrapping
    int RepeatTime = 40;
    int T;
    Matrix AAR_avg;
    Matrix CAAR_avg;
    Matrix AAR_std;
    Matrix CAAR_std;

public:
    Bootstrap() {}
    Matrix GetAvgAAR() { return AAR_avg;}
    Matrix GetAvgCAAR() { return CAAR_avg; }
    Matrix GetAARstd() { return AAR_std; }
    Matrix GetCAARstd() { return CAAR_std; }

    void SetSampleNum(int SampleNum_) { SampleNum = SampleNum_;}
    void SetRepeatTime(int RepeatTime_) {RepeatTime = RepeatTime_;}
    vector<Vector> SampledAAR(map<string, Stock*>& stocks, vector<vector<string>> grouped_stocks);
    vector<Vector> SampledCAAR(vector<Vector>& sampledAAR);
    void CalculationByBootstrapping(map<string, Stock*>& stocks);
    void Display(int groupnum);
};
