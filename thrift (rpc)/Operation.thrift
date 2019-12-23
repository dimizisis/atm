
struct Request {
  1: string username,
  2: i16 pin,
  3: optional i32 amount,
  4: optional i16 new_pin
}

service OperationService{

   string withdraw(1: Request request)
   
   string deposit(1: Request request)
   
   string get_balance(1: Request request)
   
   string change_pin(1: Request request)

}

