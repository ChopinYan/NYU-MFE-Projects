// File name: ProcessAnnoucement.h
// Author: Team 2
// Class: FRE-GY 6883
// Assignment Number: Final Project
// Honor statement: We have neither given nor received help on this assignment

#pragma once
#include <map>
#include "stock.h"

#define EOD_FILE "Russell3000EarningsAnnouncements.csv" 

map<string,Stock*> excel_reader(string filename);
