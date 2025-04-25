#include<stdio.h>
int main()
{
	int arr[5] = { 1,2,3,4,5 };
	int* p1 = arr;
	int i = 0;
	for (i = 0; i < 5; i++)
	{
		printf("%d ", *p1);
		p1++;
	}
	printf("\n");
	int b = 10;
	int* p2 = &b;
	(*p2)++;
	printf("%d", *p2);
	printf("%d", b);

	return 0;
}