-- Get companies points, excluding those that are already expired or spent
DELIMITER //
CREATE PROCEDURE Points_GetByCompany(IN id INT)
    BEGIN

        --  Return value
        DECLARE total INT DEFAULT 0;

        -- Aggregation to get sum of points
        SELECT 
            SUM(awarded_points - spent_points)
        INTO
            total
        FROM 
            points 
        WHERE
            valid_until >= CURDATE() AND company_id = id
        GROUP BY
            company_id;

        -- Result
        SELECT total;
    END//
DELIMITER ;

-- Create an order, and subtract points
DELIMITER //
CREATE PROCEDURE Orders_CreateOrder(IN company_idP INT, IN address_idP INT, IN product_idP INT, IN quantityP INT)
    BEGIN

        -- Variables
        DECLARE total_points INT DEFAULT 0;
        DECLARE subtracted INT DEFAULT 0;
        DECLARE oldest_points INT DEFAULT 0;
        DECLARE invoice VARCHAR(50) DEFAULT '';
        DECLARE points INT DEFAULT 0;

        -- Insert new order
        INSERT INTO orders (company_id, address_id, product_id, quantity, created_at, status) VALUES
        (company_idP, address_idP, product_idP, quantityP, CURDATE(), 'processed');

        -- Get total of points to subtract
        SELECT (product_unit_price * quantityP) INTO total_points FROM products WHERE product_id = product_idP;

        -- Substract points frpm oldest to newest expiration date
        WHILE subtracted < total_points DO

            -- Get oldest available points
            SELECT
                (awarded_points - spent_points), invoice_id 
            INTO
                oldest_points, invoice 
            FROM
                points 
            WHERE
                company_id = company_idP AND valid_until >= CURDATE() AND (awarded_points - spent_points) <> 0
            ORDER BY
                valid_until
            LIMIT
                1;

            -- If there are more than enough, subtract them and end procedure
            IF oldest_points >= (total_points - subtracted) THEN
                UPDATE
                    points
                SET
                    spent_points = spent_points + (total_points - subtracted)
                WHERE
                    invoice_id = invoice;
                
                -- Completed
                SET subtracted = total_points;
            ELSE
                UPDATE
                    points
                SET
                    spent_points = awarded_points
                WHERE
                    invoice_id = invoice;

                -- Add to subtracted variable
                SET subtracted = subtracted + oldest_points;
            END IF;

        END WHILE;

        -- Get new quantity of points
        CALL Points_GetByCompany(company_idP);

    END//
DELIMITER ;