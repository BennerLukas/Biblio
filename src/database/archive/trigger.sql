DROP TRIGGER IF EXISTS book_returned ON BORROW_ITEM;

CREATE TRIGGER book_returned 
AFTER UPDATE
ON borrow_item
FOR EACH ROW
EXECUTE PROCEDURE book_returned_triggered();


CREATE OR REPLACE FUNCTION book_returned_triggered()
	RETURNS TRIGGER
	LANGUAGE PLPGSQL
	AS '
		BEGIN			
			IF new.b_active <> old.b_active then
				UPDATE books
			   SET b_is_availalbe = true
		   	WHERE books.n_book_id = new.n_book_id;
	   	END if;
	   	
	   	RETURN NEW;
		END;
		';
	