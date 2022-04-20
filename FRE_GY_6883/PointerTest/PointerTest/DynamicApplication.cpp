// PointerTest.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
using namespace std;

// issue in the function
int* getNum1()
{
    int num = 10;  // num is a local variable
    num += 1;
    return &num;  // its address is not reliable once the function is complete (undefined behavior)
}  // num will be detroyed once function call is completed


// no issue
int getNum2()
{
    int num = 10;
    num += 1;
    return num;  // the value of num is cpoied and the copy is returned to main function
}


// call by pointer, no issue 
void getNum3(int* ptr)  // address of y is passed to pointer ptr
{
    *ptr += 1;
}


// issue in the function
int* getNum4()
{
    int* ptr = new int;  // dynamic allocation
    *ptr = 10;  // dereference and assign to 10
    *ptr += 1;  // dereference and add 1
    // delete ptr;  // cannot free memory inside the function as the pointer will be used in main as ptr2
    // ptr = NULL;  // cannot set the pointer to NULL as its value will be used in main as ptr2
    return ptr;
}


int main()
{
    // funtion 1
    // int* ptr1 = getNum1(); function 1 has issue

    // function 2
    int x = getNum2();
    x += 1;
    cout << "x=" << x << endl;  // 12

    // function 3
    int y = 10;
    getNum3(&y);
    y += 1;
    cout << "y=" << y << endl;  // 12

    // function 4
    int* ptr2 = nullptr;
    ptr2 = getNum4();  // ptr2 is pointing to the allocated memory
    *ptr2 += 1;
    cout << "*ptr2=" << *ptr2 << endl;  // 12; after comment out 2 lines in getNum4()
    delete ptr2;  // free allocated memory
    ptr2 = NULL;  // prevent dangling

    return 0;
}


// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
