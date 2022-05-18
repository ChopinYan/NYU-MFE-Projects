// File name: stock.h
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment

#pragma once
#include <vector>
#include <map>
#include <iostream>

using namespace std;

class Stock
// This class includes all the information for a single stock.
// Including its price and corresponding benchmark prices within a given range of time interval
{
private:
    // string variables: for dates and stock_names.
    string ticker, ann_date, start_date, end_date;
    
    // double variables: for eps and suprises.
    double estm_eps, rept_eps;
    double surprise, surprise_pct; 
    
    // int variables: label of beat, meet and miss groups, 
    // and index of start and end date in the vector of benckmark.
    int group_label, ann_date_index, start_date_index, end_date_index;

    // vector of trading dates (period) within the range of before and after the given ann_date.
    vector<string> date_range;

    // vector of stock prices and returns and corresponding benckmark prices and returns
    // within the given trading dates (period)
    vector<double> stk_prices, stk_returns, bmk_prices, bmk_returns;
    vector<double> cum_returns, abn_returns;

public:
    
    Stock() {}
    // constructor by ticker name
    Stock(string ticker_) { ticker = ticker_; }
    
    // member functions for extracting private members
    string GetTicker() { return ticker; }
    string GetAnnDate() { return ann_date; }
    string GetStartDate() { return start_date; }
    string GetEndDate() { return end_date; }
    
    double GetReptEPS() { return rept_eps; }
    double GetEstmEPS() { return estm_eps; }
    double GetSurprise() { return surprise; }
    double GetSurprisePct() { return surprise_pct; }

    int GetGroupLabel() { return group_label; } 
    vector<double> GetStkPrices() { return stk_prices; }
    vector<double> GetStkReturns() { return stk_returns; }
    vector<double> GetCumReturns() { return cum_returns; }
    vector<double> GetAbnReturns() { return abn_returns; }

    // member functions for modifying private members
    void SetTicker(string ticker_) { ticker = ticker_; }
    void SetAnnDate(string ann_date_) { ann_date = ann_date_; }
    void SetStartDate(string start_date_) { start_date = start_date_; }
    void SetEndDate(string end_date_) { end_date = end_date_; }
    
    void SetEstmEPS(double estm_eps_) { estm_eps = estm_eps_; }
    void SetReptEPS(double rept_eps_) { rept_eps = rept_eps_; }
    void SetSurprise(double surprise_) { surprise = surprise_; }
    void SetSurprisePct(double surprise_pct_) { surprise_pct = surprise_pct_; }
    
    void SetGroupLabel(int group_label_) { group_label = group_label_; }
   
    void SetDateRange(vector<string> date_range_) { date_range = date_range_; }

    void SetStkPrices(vector<double> stk_prices_) { stk_prices = stk_prices_; }
    void SetBmkPrices(vector<double> bmk_prices_) { bmk_prices = bmk_prices_; }
   
    // Calculate daily stock returns and abnormal returns
    void CalcReturns();


    // cout for case2
    void Display(int N);
};