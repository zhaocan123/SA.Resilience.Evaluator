struct Books
{
   float price;
   int   book_id;
} book = {100.5, 123456};
 
int main()
{
    int a = book.book_id;
    float b = book.price;
}