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