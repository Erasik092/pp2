-- Задача 2: Вставить или обновить (Upsert)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM PhoneBook WHERE user_name = p_name) THEN
        UPDATE PhoneBook SET phone_number = p_phone WHERE user_name = p_name;
    ELSE
        INSERT INTO PhoneBook (user_name, phone_number) VALUES (p_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Задача 3: Вставка множества пользователей с валидацией
-- Мы принимаем два массива: имен и телефонов
CREATE OR REPLACE PROCEDURE insert_many_contacts(p_names VARCHAR[], p_phones VARCHAR[])
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(p_names, 1) LOOP
        -- Простая валидация: номер должен быть длиннее 5 символов
        IF length(p_phones[i]) >= 5 THEN
            INSERT INTO PhoneBook (user_name, phone_number) 
            VALUES (p_names[i], p_phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone for user %: %', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Задача 5: Удаление по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact_adv(p_search VARCHAR)
AS $$
BEGIN
    DELETE FROM PhoneBook 
    WHERE user_name = p_search OR phone_number = p_search;
END;
$$ LANGUAGE plpgsql;