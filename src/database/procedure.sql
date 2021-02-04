--DROP PROCEDURE new_loan(INT, INT[], INT);
create or replace procedure new_loan(
    loan_user int,
    book_ids INT[],
    duration int
)
language plpgsql
AS '
		DECLARE
			book INT;
			loan_id INT;
    	BEGIN

        	INSERT INTO LOAN (ts_now, n_user_id)
        	VALUES(now(), loan_user)
        	RETURNING n_loan_id INTO loan_id;
			
			
		   FOREACH book IN ARRAY $2
			LOOP
        		INSERT INTO BORROW_ITEM (n_duration, n_book_id, n_loan_id)
        		VALUES (duration, book,loan_id);
        		
        		UPDATE books
	        	SET b_is_availalbe = false
   	     	WHERE n_book_id = book;
        	END loop;

        
        
		END;
	';
	
-- Test
-- CALL new_loan(1,ARRAY[1,2,3],31);

