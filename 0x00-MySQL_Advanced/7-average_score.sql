-- average score

DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser$$
CREATE PROCEDURE ComputeAverageScoreForUser(IN users_id INT)
BEGIN
    DECLARE average_score FLOAT;
    SELECT AVG(score) INTO average_score FROM corrections
    WHERE user_id = users_id;

    UPDATE users
    SET average_score = average_score
    WHERE id = users_id;
END//
DELIMITER ;
