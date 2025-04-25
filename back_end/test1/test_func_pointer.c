int Max(int, int);  
int main(void)
{
    int(*p)(int, int); 
    int a=1;
    int b=2;
    int c;
    p = Max;
    c = (*p)(a, b); 
    return 0;
}
int Max(int x, int y)
{
    int z;
    if (x > y)
    {
        z = x;
    }
    else
    {
        z = y;
    }
    return z;
}