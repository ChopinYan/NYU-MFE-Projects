// File name: gnuplot.cpp
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment

#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "Gnuplot.h"
using namespace std;

void plotGnuplot(Matrix& CAAR_avg) {
    int i;
    int nIntervals = CAAR_avg[0].size();
    int intervalSize = CAAR_avg[0].size();
    int stepSize = 1;
    double* xData = (double*)malloc((nIntervals) * sizeof(double));
    double* yData0 = (double*)malloc((nIntervals) * sizeof(double));
    double* yData1 = (double*)malloc((nIntervals) * sizeof(double));
    double* yData2 = (double*)malloc((nIntervals) * sizeof(double));
    int index = (int) ( - (nIntervals - 1) * 0.5);
    xData[0] = index;
    for (i = 0; i < nIntervals - 1; i++) {
        double x0 = xData[i];
        xData[i + 1] = x0 + stepSize;
    }
    for (i = 0; i < nIntervals; i++) {

        yData0[i] = CAAR_avg[0][i];
    }
    for (i = 0; i < nIntervals; i++) {

        yData1[i] = CAAR_avg[1][i];
    }
    for (i = 0; i < nIntervals; i++) {

        yData2[i] = CAAR_avg[2][i];
    }
    FILE* gnuplotPipe, * tempDataFile;

    const char* tempDataFileName0 = "Miss group";
    const char* tempDataFileName1 = "Meet group";
    const char* tempDataFileName2 = "Beat group";
    double x0, y0, x1, y1, x2, y2;
    gnuplotPipe = _popen("C:\\PROGRA~1\\gnuplot\\bin\\gnuplot.exe", "w");//pc dir
    //gnuplotPipe = popen("/opt/local/bin/gnuplot","w");//mac dir
    if (gnuplotPipe) {
        fprintf(gnuplotPipe, "plot \"%s\" with lines, \"%s\" with lines,\"%s\" with lines\n", tempDataFileName2, tempDataFileName1, tempDataFileName0);

        fflush(gnuplotPipe);


        tempDataFile = fopen(tempDataFileName0, "w");
        for (i = 0; i < intervalSize; i++) {
            x0 = xData[i];
            y0 = yData0[i];
            fprintf(tempDataFile, "%lf %lf\n", x0, y0);
        }
        fclose(tempDataFile);

        tempDataFile = fopen(tempDataFileName2, "w");
        for (i = 0; i < intervalSize; i++) {
            x2 = xData[i];
            y2 = yData2[i];
            fprintf(tempDataFile, "%lf %lf\n", x2, y2);
        }
        fclose(tempDataFile);

        tempDataFile = fopen(tempDataFileName1, "w");
        for (i = 0; i < intervalSize; i++) {
            x1 = xData[i];
            y1 = yData1[i];
            fprintf(tempDataFile,"%lf %lf\n", x1, y1);
        }

        fclose(tempDataFile);



        printf("press enter to continue...");
        getchar();
        remove(tempDataFileName0);
        remove(tempDataFileName1);
        remove(tempDataFileName2);

    }
    else {
        printf("gnuplot not found...");
    }

    delete yData0;
    delete yData1;
    delete yData2;
    delete xData;
    yData0 = nullptr;
    yData1 = nullptr;
    yData2 = nullptr;
    xData = nullptr;

}