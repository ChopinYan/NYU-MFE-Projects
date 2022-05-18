// File name: ProcessAnnouncement.cpp
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment

#include "ProcessAnnoucement.h"
#include <algorithm>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <sstream>
#include <vector>
using namespace std;


void parse_date_format(string &s) {
    string delimiter = "-";
    string date = s.substr(0, s.find(delimiter));
    s.erase(0, s.find(delimiter) + delimiter.length());
    string month = s.substr(0, s.find(delimiter));
    s.erase(0, s.find(delimiter) + delimiter.length());
    string year = "20" + s.substr(0, s.find(delimiter));

    const int total_month = 12;
    string monthNames[total_month] = { "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC" };
    for (int cur_month = 0; cur_month < total_month; cur_month++) {
        if (month == monthNames[cur_month]) {
            if (cur_month >= 9) {
                month = to_string(cur_month + 1);
            }
            else {
                month = "0" + to_string(cur_month + 1);
            }
        }
    }
    s = year + "-" + month + "-" + date;
}

void calculate_thresholds(string f_n, double& f, double& s, int& fdup, int& sdup)
{
    // construct an ifstream object to read information from files
    ifstream fin;
    fin.open(f_n, ios::in);
    if (!fin.is_open()) {
        cerr << "Error: could not open EarningAnnouncements.csv" << endl;
        system("pause");
    }

    string line;
    getline(fin, line); //skip the first line here

    vector<double> surprise_list;
    while (getline(fin, line)) {
        istringstream ss_line(line);
        string item = "";
        for (int i = 0; i < 6; i++) {
            getline(ss_line, item, ',');
        }
        getline(ss_line, item, ',');
        double percent = stod(item);
        surprise_list.push_back(percent);
    }

    sort(surprise_list.begin(), surprise_list.end());
    double bar = surprise_list.size() / 3.0;
    f = surprise_list[(int)bar];
    s = surprise_list[(int)(2 * bar)];
    fdup = count(surprise_list.begin(), surprise_list.end(), f) / 2;
    sdup = count(surprise_list.begin(), surprise_list.end(), s) / 2;

}

map<string, Stock*> excel_reader(string filename)
{
    double first, second;
    int f_dup, s_dup;
    // int f_num, s_num, t_num;
    // calculate_thresholds(filename, first, second, f_num, s_num, t_num);
    calculate_thresholds(filename, first, second, f_dup, s_dup);

    string line, symbol, announce_date, announce_date_end, estimated_eps, reported_eps, surprise_eps, surprise_percentage;
    double destimated, dreported, dsurprise, dsurprise_percentage;
    ifstream fin;
    fin.open(filename, ios::in);
    if (!fin.is_open()) {
        cerr << "Open EarningsAnnouncements.csv Failed" << endl;
        system("pause");
    }
    getline(fin, line);

    map<string, Stock*> stock_list;

    while (!fin.eof()) {
        Stock* stk = new Stock();
        getline(fin, line);
        if (!line.empty()) {
            stringstream ss_line(line);
            getline(ss_line, symbol, ',');
            getline(ss_line, announce_date, ',');
            getline(ss_line, announce_date_end, ',');
            getline(ss_line, estimated_eps, ',');
            getline(ss_line, reported_eps, ',');
            getline(ss_line, surprise_eps, ',');
            getline(ss_line, surprise_percentage, ',');

            destimated = strtod(estimated_eps.c_str(), NULL);
            dreported = strtod(reported_eps.c_str(), NULL);
            dsurprise = strtod(surprise_eps.c_str(), NULL);
            dsurprise_percentage = strtod(surprise_percentage.c_str(), NULL);


            parse_date_format(announce_date);
            stk->SetTicker(symbol);
            stk->SetAnnDate(announce_date);
            stk->SetEndDate(announce_date_end);
            stk->SetEstmEPS(destimated);
            stk->SetReptEPS(dreported);
            stk->SetSurprise(dsurprise);
            stk->SetSurprisePct(dsurprise_percentage);


            if (dsurprise_percentage < first) {
                stk->SetGroupLabel(1);
      

            }
            else if (dsurprise_percentage >= first && dsurprise_percentage < second) {
                if (dsurprise_percentage == first && f_dup > 0) {
                    stk->SetGroupLabel(1);
                    f_dup--;
                }
                else {
                    stk->SetGroupLabel(2);
                }
            }
            else
            {
                if (dsurprise_percentage == second && s_dup > 0) {
                    stk->SetGroupLabel(2);
                    s_dup--;
                }
                else {
                    stk->SetGroupLabel(3);
                }
            }

            stock_list[symbol] = stk;
        }
    }
    return stock_list;
}
