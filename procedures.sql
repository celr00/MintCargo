-- Get companies points, excluding those that are already expired or spent

DELIMITER //
CREATE PROCEDURE Points_GetByCompany(IN id INT)
    BEGIN
        DECLARE total INT DEFAULT 0;
        SELECT 
            SUM(awarded_points - spent_points)
        INTO
            total
        FROM 
            points 
        WHERE
            valid_until > CURDATE() AND company_id = id
        GROUP BY
            company_id;
        SELECT total;
    END//
DELIMITER ;