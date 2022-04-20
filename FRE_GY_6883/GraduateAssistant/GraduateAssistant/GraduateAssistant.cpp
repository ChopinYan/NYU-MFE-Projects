// GraduateAssistant.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
// Virtual Inheritence


#include <iostream>
using namespace std;
class Person
{
public:
	int GetAge() const { return age; }
	int GetId() const { return id; }
	void SetAge(int age_) { age = age_; }
	void SetId(int id_) { id = id_; }
private:
	int age;
	int id;
};
class Student : public virtual Person
{
public:
	double GetGPA() const { return gpa; };
	void SetGPA(double gpa_) { gpa = gpa_; }
private:
	double gpa;
};
class Employee : public virtual Person
{
public:
	double GetSalary() const { return salary; }
	void SetSalary(double salary_) { salary = salary_; }
private:
	double salary;
};
class GradAssistant : public Student, public Employee
{
public:
	void Display() const;
};
void GradAssistant::Display() const
{
	cout << GetId() << "," << GetAge() << ","
		<< GetGPA() << "," << GetSalary() << endl;
}
int main()
{
	GradAssistant GA;
	GA.SetId(12345);
	GA.SetAge(25);
	GA.SetGPA(4.0);
	GA.SetSalary(500000);
	GA.Display();
	return 0;
}

