
#include <iostream>
using namespace std;
 
int main ()
{
   // 局部变量声明
   char grade = 'D';
   int a = -1;
 
   switch(grade)
   {
   case 'A' :
      a= 0;
      break;
   case 'B' :
     a = -3;
     break;
   case 'C' :
      a = 1;
      break;
   case 'D' :
      a = 2;
      break;
   case 'F' :
      a = 3;
      break;
   default :
      a = 99;
   }
   a++;
 
   return 0;
}
