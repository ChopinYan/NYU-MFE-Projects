// File name: libcurl.h
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment


#pragma once
#include <vector> 
#include <map>
#include "curl/curl.h"
#include "stock.h"
#include "ProcessAnnoucement.h"
using namespace std;

struct MemoryStruct
{
    char* memory;
    size_t size;
};

void* myrealloc(void* ptr, size_t size);
size_t write_data(void* ptr, size_t size, size_t nmemb, void* data);
map<string, double> fetch_benchmark_price(Stock* benchmark); // fetch benchmark price first

int stock_data_processor(map<string, double> benchmark_map, vector<string> valid_dates, int number, int stock_count);
void multithread_handler(map<string, Stock*>& stocks, map<string, double> benchmark_map, vector<string> valid_dates, int number);
bool isNumber(const string& str);
map<string, Stock*> initialize_with_data(string& s_num, Stock* benchmark);
