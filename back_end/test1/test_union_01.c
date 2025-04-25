union Data
{
   int i;
   float f;
};
 
int main( )
{
   union Data data;        
   int a = data.i;
   float b = data.f;
   return 0;
}