-- 1. Add phone
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE cid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_contact_name;

    IF cid IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (cid, p_phone, p_type);
END;
$$;


-- 2. Move to group (auto-create group)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE cid INT;
DECLARE gid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_contact_name;

    IF cid IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    SELECT id INTO gid FROM groups WHERE name = p_group_name;

    IF gid IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name) RETURNING id INTO gid;
    END IF;

    UPDATE contacts SET group_id = gid WHERE id = cid;
END;
$$;


-- 3. Extended search (name + email + phones)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id INT,
    name TEXT,
    email TEXT,
    phone TEXT,
    group_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.email, p.phone, g.name
    FROM contacts c
    LEFT JOIN phones p ON p.contact_id = c.id
    LEFT JOIN groups g ON g.id = c.group_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$;