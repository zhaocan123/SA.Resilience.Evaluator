#include<stdio.h>
int main()
{
	int x = 1;
	int y = 2;
	int* p = &x;
	if (x == 1)
	{
		int* p = &y;
		printf("%d ", *p);
	}
	printf("%d ", *p);
	return 0;
}