#include<stdio.h>
int main()
{
	int arr[5] = { 1,2,3,4,5 };
	int x = 1;
	int* p1 = &arr[1];
	int* p3 = &x;
	int i = 0;
	for (i = 0; i < 5; i++)
	{
		printf("%d ", *p1);
		p1++;
	}
	printf("%d ", *(p1 - x));
	printf("\n");
	p1 = p3;
	p3 = arr;

	int b = *p1;
	int* p2 = &b;
	(*p2)++;
	printf("%d", *p2);
	printf("%d", b);

	return 0;
}