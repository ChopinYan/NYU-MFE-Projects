// List.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <list>
using namespace std;

int main()
{
	list<int> l(5, 10);
	for (list<int>::iterator itr = l.begin(); itr != l.end(); itr++)
	{
		cout << *itr << " " << endl;
	}

}

/*
10
10
10
10
10
*/
