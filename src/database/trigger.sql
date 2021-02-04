DROP TRIGGER IF EXISTS loan_happened ON LOAN;
CREATE TRIGGER loan_happened
AFTER INSERT 
ON LOAN 
FOR EACH ROW
EXECUTE procedure last_not_available();

