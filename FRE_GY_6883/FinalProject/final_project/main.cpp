// File name: main.cpp
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


void ticker_check(map<string, Stock*>& stks, string& t) {
    while (!stks[t]) {
        cout << "Invalid Ticker Name. Re-Enter Here: ";
        cin >> t;
        getchar();
        // make input uppercase
        for (auto& c : t) c = toupper(c);
        cout << endl;
    }
}

int main()
{
    //cout << "Welcome to Russell1000 Earnings Surprise Impact Detecting System!" << endl << endl;
    //cout << "Press any button to start loading Russell 1000 stock data from csv file...." << endl;
    //getchar();

    // Initialization
    Stock* benchmark = new Stock("IWV"); // this is a dynamic allocation
    map<string, double> benchmark_map;
    Bootstrap bts;
    int option;  // 
    string soption;  // 
    string snumber;
    bool cont = true;  // WHILE LOOP
    string ticker;
    string sgroup;
    // vector<double> X;

    /*
    Developer Note
    This is for testing the functionalities of the program. To ensure that our data is complete,
    please uncomment the following block. A menu will be prompted when all tests are done.
    */
 
    /*cout << "Running Tests:" << endl;
    int test_res = run_tests();
    if(test_res == 0)
    {
        cout << "All Tests Passed Successfully!" << endl;
    }*/


    // MENU
    map<string, Stock*> stocks = initialize_with_data(snumber, benchmark);
    bts.CalculationByBootstrapping(stocks);

    while (cont) {
        //cout << "Final Project Group 2" << endl;
        //cout << endl;
        cout << "------------------------------MENU------------------------------" << endl;
        cout << "1. Change the existing number N" << endl;
        cout << "2. Pull info of a single stock" << endl;
        cout << "3. Show AAR, AAR-STD, CAAR and CAAR-STD for one group" << endl;
        cout << "4. Show the gnuplot graph with CAAR for all 3 groups" << endl;
        cout << "5. Exit" << endl << endl;
        cout << "Please Enter Number 1-5: ";
        cin >> soption;
        getchar();
        cout << endl << endl;

        while ((soption.at(0) > '5' || soption.at(0) <= '0')) {
            cout << "Input a Number from 1 to 5 only" << endl;
            cout << "1. Change the existing number N" << endl;
            cout << "2. Pull info of a single stock" << endl;
            cout << "3. Show AAR, AAR-STD, CAAR and CAAR-STD for one group" << endl;
            cout << "4. Show the gnuplot graph with CAAR for all 3 groups" << endl;
            cout << "5. Exit" << endl << endl;
            cout << "Please Enter Number 1-5: ";
            cin >> soption;
            getchar();
            cout << endl << endl;
        }

        option = stoi(soption);
        switch (option) {

            case 1: {
                stocks = initialize_with_data(snumber, benchmark);
                bts.CalculationByBootstrapping(stocks);
                break; 
            }

            case 2: {
                cout << "Pull information for one stock." << endl;
                cout << "Please enter stock ticker: ";
                cin >> ticker;
                getchar();
                cout << endl;
                for (auto& c : ticker) c = toupper(c);
                ticker_check(stocks, ticker);
                stocks[ticker]->Display(stoi(snumber));
                break;
            }

            case 3: {
                cout << "Please enter the group selection: " << endl
                    << "1. Miss group" << endl
                    << "2. Meet group" << endl
                    << "3. Beat group" << endl
                    << endl;
                cout << "Please Enter Number 1-3: ";
                cin >> sgroup;
                getchar();
                cout << endl;

                while ((sgroup.at(0) > '3' || sgroup.at(0) <= '0')) {
                    cout << "Input a Number from 1 to 5 only" << endl << endl;
                    cout << "Please enter the group selection: " << endl
                        << "1. Miss group" << endl
                        << "2. Meet group" << endl
                        << "3. Beat group" << endl
                        << endl;
                    cout << "Please Enter Number 1-3: ";
                    cin >> sgroup;
                    getchar();
                    cout << endl;
                }
                bts.Display(stoi(sgroup) - 1);
                break; 
            }

            case 4: {
                Matrix a = bts.GetAvgCAAR();
                cout << "Done. Check Figure." << endl << endl;
                plotGnuplot(a);
                break; 
            }
                        
            case 5: {

                for (map<string, Stock*> ::iterator itr = stocks.begin(); itr != stocks.end(); itr++)
                {
                    delete itr->second;
                }
                delete benchmark;
                benchmark = NULL;

                cont = false; // BREAK WHILE LOOP: EXIT
                cout << "Program exited." << endl << endl;
                break;
            }
            return 0;
        };                 
    };
}