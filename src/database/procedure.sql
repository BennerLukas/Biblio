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




-- create or replace procedure last_not_available(
-- )
-- language plpgsql
-- as '
--     BEGIN
--         UPDATE books
--         SET b_is_availalbe = false
--         WHERE n_book_id = (SELECT n_book_id FROM borrow_item WHERE n_loan_id = (SELECT n_loan_id FROM LOAN ORDER BY n_loan_id DESC LIMIT 1));
--     COMMIT; 
-- 	end;'


create or replace function last_not_available()
RETURNS TRIGGER
language plpgsql
as '
   BEGIN
        UPDATE books
        SET b_is_availalbe = false
        WHERE n_book_id = (SELECT n_book_id FROM borrow_item WHERE n_loan_id = (SELECT n_loan_id FROM LOAN ORDER BY n_loan_id DESC LIMIT 1));
	END;'


CREATE TRIGGER loan_happened
AFTER INSERT 
ON LOAN 
FOR EACH ROW
EXECUTE procedure last_not_available();



