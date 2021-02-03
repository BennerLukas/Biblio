-- if loan happened --> change is available
create or replace procedure new_loan(
    loan_user int,
    book int,
    duration int
)
language plpgsql
as '
    BEGIN

        INSERT INTO LOAN (ts_now, n_user_id)
        VALUES(now(), loan_user);
       
    
        INSERT INTO BORROW_ITEM (n_duration, n_book_id, n_loan_id)
        VALUES (duration, book,(SELECT n_loan_id FROM LOAN ORDER BY n_loan_id DESC LIMIT 1));
    COMMIT; 

	end;'

create or replace procedure not_available(
    loan_user int,
    book int,
    duration int
)
language plpgsql
as '
    BEGIN
        SELECT n_book_id FROM borrow_item WHERE n_loan_id = (SELECT n_loan_id FROM LOAN ORDER BY n_loan_id DESC LIMIT 1);

       
    COMMIT; 

	end;'





CREATE TRIGGER loan_happened
AFTER INSERT 
ON LOAN 
FOR EACH ROW
EXECUTE procedure