enum DAY
{
      MON=1, TUE, WED, THU, FRI, SAT, SUN
} day;
int main()
{
    int a = 0;
    for (day = MON; day <= SUN; day++) {
        a = day;
    }
}