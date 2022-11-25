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

-- Create an order, and substract points
DELIMITER //
CREATE PROCEDURE Orders_CreateOrder(IN company_idP INT, IN product_idP INT, IN quantityP INT)
    BEGIN

        -- Order
        INSERT INTO orders (company_id, created_at, status) VALUES
        (company_idP, CURDATE(), 'processed');

        -- Get order ID and points_spent
        DECLARE created_order_id INT;
        SELECT TOP 1 order_id INTO created_order_id FROM orders ORDER BY order_id DESC;
        DECLARE spent INT DEFAULT 0;
        SELECT product_unit_price*quantityP INTO spent FROM products WHERE product_id = product_idP;

        -- Order details
        INSERT INTO order_details VALUES
        (created_order_id, product_idP, quantityP, spent);

        -- Substract points
        

    END//
DELIMITER ;