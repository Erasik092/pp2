-- Задача 1: Поиск по паттерну (имя или телефон)
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(pattern TEXT)
RETURNS TABLE (id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT user_id, user_name, phone_number 
    FROM PhoneBook
    WHERE user_name ILIKE '%' || pattern || '%' 
       OR phone_number ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- Задача 4: Пагинация
CREATE OR REPLACE FUNCTION get_contacts_paged(p_limit INT, p_offset INT)
RETURNS TABLE (id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT user_id, user_name, phone_number 
    FROM PhoneBook
    ORDER BY user_id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;