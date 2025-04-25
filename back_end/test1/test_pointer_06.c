#include<stdio.h>
int main()
{
	int x = 1;
	int y = 2;
	int z = 3;
	int* p1;
	if (x <= 1)
	{
		p1 = &y;
	}
	else
	{
		p1 = &z;
	}

	int* p2 = p1;
	printf("%d", *p2);
}