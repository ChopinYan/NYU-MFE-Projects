// File name: libcurl.cpp
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment

#include "libcurl.h"
#include "stock.h"
#include <algorithm>
#include <string>
#include <thread>
#include <queue>
#include <stdio.h>
#include <string>
#include <iostream>
#include <sstream>
#include <vector>
#include <locale>
#include <iomanip>
#include <thread>
// #include <condition_variable>
#include <time.h>
using namespace std;

// libcurl information
#define TOKEN "626dc3b898adc9.54483444"
#define URL "https://eodhistoricaldata.com/api/eod/" 


// Calculate the optimal(max) number of cores to be used 
const int cores = int(thread::hardware_concurrency());
#define THREAD_NUM cores

// Progress bar formatting
#define PBSTR "||||||||||||||||||||||||||||||||||||||||||||||||||"
#define PBWIDTH 50
int cur_stk = 0;  // progress bar percentage setting

// The queue data structure follows the FIFO principle.
// it is used for the temporary storage and the convenience of member assignment for the object.
queue<Stock*> stockq;

// This includes a list of stocks where announcement dates are not trading days.
vector<string> fail_list;


void* myrealloc(void* ptr, size_t size)
{
    // reallocates a block of memory that was previously allocated but not yet freed
    if (ptr) return realloc(ptr, size);
    // allocates a block of uninitialized memory to a pointer
    else return malloc(size);
}

size_t write_data(void* ptr, size_t size, size_t nmemb, void* data)
{
    size_t realsize = size * nmemb;
    // get the pointer of the MemooryStruct
    struct MemoryStruct* mem = (struct MemoryStruct*)data;
    // updates the size of memory the pointer points to
    mem->memory = (char*)myrealloc(mem->memory, mem->size + realsize + 1);
    if (mem->memory)
    {
        // copy the data to the mem->memory with the mem->size position
        memcpy(&(mem->memory[mem->size]), ptr, realsize);
        mem->size += realsize;
        // zero termination of the data
        mem->memory[mem->size] = 0;
    }
    return realsize;
}


// printing the progress bar
void progress_bar(double p) {
    if (p >= 0) {
        int val = (int)(p * 100);
        int lpad = (int)(p * PBWIDTH);
        int rpad = PBWIDTH - lpad;
        printf("\r%3d%% [%.*s%*s]", val, lpad, PBSTR, rpad, "");
        fflush(stdout);
    }
}

map<string, double> fetch_benchmark_price(Stock* benchmark)
{   
    // check if IWV is set as our benchmark
    //if ((benchmark->GetTicker()) != "IWV") {
    //    if ((benchmark->GetTicker()) == "TEST") {
    //        cout << "Test Passed. Ignore this message." << endl;
    //    }
    //    else {
    //        cerr << "Benchmark is supposed to be 'IWV'." << endl;
    //        system("pause");
    //    }
    //}

    // declaration of a pointer to an curl object
    CURL* handle;
    CURLcode result;

    // set up the program environment that libcurl needs
    curl_global_init(CURL_GLOBAL_ALL);

    // curl_easy_init() returns a CURL easy handle
    handle = curl_easy_init();

    // map to store the price of benchmark on each trade date
    map<string, double> bmk_map;

    // if everything's all right with the easy handle...
    if (handle)
    {
        string url_common = URL;
        string api_token = TOKEN;
        string start_date = "2021-01-01";
        string end_date = "2022-05-01";
        
        struct MemoryStruct data;
        data.memory = NULL;
        data.size = 0;

        string symbol = benchmark->GetTicker();
        string url_request = url_common + symbol + ".US?" + "from=" + start_date + "&to=" + end_date + "&api_token=" + api_token + "&period=d";
        curl_easy_setopt(handle, CURLOPT_URL, url_request.c_str());

        // adding a user agent
        curl_easy_setopt(handle, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0");
        curl_easy_setopt(handle, CURLOPT_SSL_VERIFYPEER, 0);
        curl_easy_setopt(handle, CURLOPT_SSL_VERIFYHOST, 0);

        // pass a pointer to the callback function
        // ptr points to the delivered data
        // all the data will be passed to the WRITEFUNCTION and stored to the memory
        curl_easy_setopt(handle, CURLOPT_WRITEFUNCTION, write_data);
        curl_easy_setopt(handle, CURLOPT_WRITEDATA, (void*)&data);

        // Successful fetchment or not
        result = curl_easy_perform(handle);

        if (result != CURLE_OK)
        {
            // if errors have occured, tell us what is wrong with result
            fprintf(stderr, "curl_easy_perform() has failed with result: %s\n", curl_easy_strerror(result));
        }

        stringstream sData;
        sData.str(data.memory);
        
        string line;
        string str_daily_stk_price, str_trade_date;
        double daily_stk_price;
        vector<string> date_range;
        vector<double> stk_prices;

        while (getline(sData, line))
        {
            // process only if data format found
            size_t found = line.find('-');
            // process until the last line of data
            if (found != std::string::npos)
            {
                // string type trade date
                str_trade_date = line.substr(0, line.find_first_of(','));
                // erase last element of the line: Volume (unuseful data)
                line.erase(line.find_last_of(','));
                // string type daily stock price
                str_daily_stk_price = line.substr(line.find_last_of(',') + 1);
                // double type daily stock price
                daily_stk_price = strtod(str_daily_stk_price.c_str(), NULL);

                // vector filling
                date_range.push_back(str_trade_date);
                stk_prices.push_back(daily_stk_price);

                // benchmark map filling
                bmk_map[str_trade_date] = daily_stk_price;
            }
        }
        // set valid trading date and corresponding benchmark prices to Stock object: benchmark
        benchmark->SetDateRange(date_range);
        benchmark->SetStkPrices(stk_prices);

        // free the dynamic data memory
        free(data.memory);
        data.size = 0;
    }
    else
    {
        fprintf(stderr, "Curl init failed!\n");
    }

    // cleanup since you've used curl_easy_init
    curl_easy_cleanup(handle);
    // release resources acquired by curl_global_init()
    curl_global_cleanup();

    return bmk_map;
}


int stock_data_processor(map<string, double> benchmark_map, vector<string> valid_dates, int number, int sc)
// :param valid_dates: the whole period of valid trading dates of benchmark fetched
// :param number: number of days N (input, from 60 to 90)
// :param sc: stock count, for progress bar: percentage of stocks extracted
{
    // size of benchmark dates (valid_dates) 
    int bmk_size = (int)valid_dates.size();

    // declaration of a pointer to an curl object
    CURL* handle;
    CURLcode result;

    // curl_easy_init() returns a CURL easy handle
    handle = curl_easy_init();

    // if everything's all right with the easy handle...
    if (handle)
    {

        while (1)
        {
            cur_stk++;
            double percentage = (cur_stk) / (double)sc;
            progress_bar(percentage);

            if (stockq.size() == 0)
            {
                // if the stockq is empty, we can unlock and clear the thread 
                curl_easy_cleanup(handle);
                return 0;
            }
            // extract the pointer from stockq
            Stock* tempstock = stockq.front();
            // pop out the element after obtaining
            stockq.pop();

            string zero_date = tempstock->GetAnnDate();
            int x = 0;
            // iterate vaild trading dates based on benchmark, 
            // if the announcement date is in the valid trading dates, return the index of that date
            for (int i = 0; i < bmk_size; i++) {
                if (valid_dates[i] == zero_date) {
                    x = i;
                }
            }
            // if x = 0, that means the announcement date is not in the valid trading dates
            // we do not fetch price data of that stock
            if (x == 0) {
                fail_list.push_back(tempstock->GetTicker());
            }
            // else, start fetching data
            else {
                string url_common = URL;
                string api_token = TOKEN;
                string start_date = valid_dates[x - number];
                string end_date = valid_dates[x + number];


                struct MemoryStruct data;
                data.memory = NULL;
                data.size = 0;
                
                string symbol = tempstock->GetTicker();
                string url_request = url_common + symbol + ".US?" + "from=" + start_date + "&to=" + end_date + "&api_token=" + api_token + "&period=d";
                curl_easy_setopt(handle, CURLOPT_URL, url_request.c_str());
                
                //adding a user agent
                curl_easy_setopt(handle, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0");
                curl_easy_setopt(handle, CURLOPT_SSL_VERIFYPEER, 0);
                curl_easy_setopt(handle, CURLOPT_SSL_VERIFYHOST, 0);
                
                curl_easy_setopt(handle, CURLOPT_WRITEFUNCTION, write_data);
                curl_easy_setopt(handle, CURLOPT_WRITEDATA, (void*)&data);
                
                // successful extraction or not
                result = curl_easy_perform(handle);
                
                if (result != CURLE_OK)
                {
                    // if errors have occured, tell us what is wrong with result
                    fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(result));
                }
                
                stringstream sData;  // read and write
                sData.str(data.memory);
                                
                string line;
                string str_daily_stk_price, str_trade_date;
                double daily_stk_price;
                vector<string> date_range;
                vector<double> stk_prices;
                vector<double> bmk_prices;
                
                try
                {
                    while (getline(sData, line))
                    {
                        // process only if data format found
                        size_t found = line.find('-');
                        // process until the last line of data
                        if (found != std::string::npos)
                        {
                            // string type trade date
                            str_trade_date = line.substr(0, line.find_first_of(','));
                            // erase last element of the line: Volume (unuseful data)
                            line.erase(line.find_last_of(','));
                            // string type daily stock price
                            str_daily_stk_price = line.substr(line.find_last_of(',') + 1);
                            // double type daily stock price
                            daily_stk_price = strtod(str_daily_stk_price.c_str(), NULL);
                                            
                            // vector filling
                            date_range.push_back(str_trade_date);
                            stk_prices.push_back(daily_stk_price);
                            bmk_prices.push_back(benchmark_map[str_trade_date]);
                        }
                    }
                
                    // Stock class object filling
                    tempstock->SetDateRange(date_range);
                    tempstock->SetStkPrices(stk_prices);
                    tempstock->SetBmkPrices(bmk_prices);
                    tempstock->CalcReturns();
                }
                catch (out_of_range& exc)
                {
                    cout << exc.what() << " Line:" << __LINE__ << " File:" << __FILE__ << endl;
                }
                catch (...)
                {
                    cout << "other error." << " Line:" << __LINE__ << " File:" << __FILE__ << endl;
                }

                free(data.memory);
                data.size = 0;
            }
        }
    }
    else
    {
        fprintf(stderr, "Curl init failed!\n");
    }

    return 0;
}


void multithread_handler(map<string, Stock*>& stocks, map<string, double> benchmark_map, vector<string> valid_dates, int number)
// Use multi-thread to download data, define the thread block to download a single stock data
// Join all the thread together to realize multi-thread downloading
{
    time_t s, e;
    s = time(NULL);
    curl_global_init(CURL_GLOBAL_ALL); // initial the global environment

    int stock_count = 0;
    for (map<string, Stock*>::iterator itr = stocks.begin(); itr != stocks.end(); itr++)
    {
        // push stock pointe to queue 
        stockq.push(itr->second);
        stock_count++;
    }

    // dynamic allocation for thread array
    thread* threads = new thread[THREAD_NUM];
    for (int i = 0; i < THREAD_NUM; i++)
    {
        threads[i] = thread(stock_data_processor, benchmark_map, valid_dates, number, stock_count);
    }
    for (int i = 0; i < THREAD_NUM; i++)
    {
        // synchronize threads
        threads[i].join();
    }
    curl_global_cleanup(); // clean up the environment

    e = time(NULL);
    double secs = difftime(e, s);
    cout << endl;
    // if there are stocks with announcement date which is not in the valid trading dates.
    cout << "Retrieved " << ((size_t)stock_count - fail_list.size()) << "/" << stock_count << " successfully." << endl;
    cout << endl;
    if (fail_list.size() != 0) {
        cout << "Failed to map:" << endl;
        for (auto i : fail_list) {
            std::cout << i << " did not annouce on regular trading dates." << endl;
        }
        fail_list.clear();
        cout << endl;
    }
    
    // delete stocks that have missing dates
    auto itr = stocks.begin();
    while (itr != stocks.end()) {
        int length = (int)itr->second->GetStkPrices().size();
        if (length < 2 * number + 1) {
            cout << itr->first << " is eliminated because there are no enough historical prices for 2N+1" << endl;
            itr = stocks.erase(itr);
        }
        else {
            ++itr;
        }
    }

    cout << secs << " seconds used in retrieving data." << endl << THREAD_NUM << " threads were used for your machine." << endl;
    cout << endl << endl;
    cur_stk = 0;
}
bool isNumber(const string& str) {
    // c: for every char in the string 
    for (char const& c : str) {
        if (std::isdigit(c) == 0) return false;
    }
    return true;
}

map<string, Stock*> initialize_with_data(string& s_num, Stock* benchmark) {
    cout << "Input a number N (60<=N<=90) to retrieve 2N+1 Days of historical EOD data" << endl;
    cout << "Please Enter: ";
    cin >> s_num;
    // s_num = getchar(); // getchar() will not ignore space, whereas cin will.
    cout << endl;

    while ((!isNumber(s_num)) || stoi(s_num) < 60 || stoi(s_num) > 90) {
        // invalid input
        cout << "Invalid Range! Input a number N (60<=N<=90)" << endl;
        cout << "Please Enter: ";
        cin >> s_num;
        // getchar();
        cout << endl;
    }

    cout << "Loading Annoucement & Benchmark(IWV) Data...";
    map<string, Stock*> stks = excel_reader(EOD_FILE);
    map<string, double> benchmark_map = fetch_benchmark_price(benchmark);
    cout << "Finished." << endl;
    cout << endl;
    cout << "Downloading Russell 3000 Data for " + s_num + " Days" << endl;
    

    vector<string> valid_dates;
    for (map<string, double>::iterator itr = benchmark_map.begin(); itr != benchmark_map.end(); itr++) {
        valid_dates.push_back(itr->first);
    }

    multithread_handler(stks, benchmark_map, valid_dates, stoi(s_num));

    return stks;
}