-- Insert the "super_user" type with all four permissions
DO $$
DECLARE
    super_user_type_id INTEGER;
    permission_id INTEGER;
BEGIN
    -- Step 1: Check and insert "super_user" type
    IF NOT EXISTS (SELECT 1 FROM type WHERE name = 'super_user') THEN
        INSERT INTO type (name, description, weight)
        VALUES ('super_user', 'Super User Type with all permissions', 1000)
        RETURNING typeId INTO super_user_type_id;
    ELSE
        -- Get the existing "super_user" type ID
        SELECT typeId INTO super_user_type_id FROM type WHERE name = 'super_user';
    END IF;

    -- Step 2: Associate all four permissions with the "super_user" type
    FOR permission_id IN (SELECT permissionId FROM permission WHERE kind IN ('Create', 'Read', 'Update', 'Delete')) LOOP
        -- Check if the permission is already associated
        IF NOT EXISTS (SELECT 1 FROM type_permission WHERE typeId = super_user_type_id AND permissionId = permission_id) THEN
            INSERT INTO type_permission (typeId, permissionId) VALUES (super_user_type_id, permission_id);
        END IF;
    END LOOP;
END $$;

-- Step 1: Relate the "super_user" role to the user "juandavidarguello@gmail.com" with the scope "TI Department ARG"
DO $$
DECLARE
    user_id INTEGER;
    super_user_role_id INTEGER;
    super_user_type_id INTEGER;
    ti_department_arg_scope_id INTEGER;
BEGIN
    -- Get the user ID for "juandavidarguello@gmail.com"
    SELECT userId INTO user_id FROM app_user WHERE username = 'juandavidarguello@gmail.com';

    -- Get the "super_user" type ID
    SELECT typeId INTO super_user_type_id FROM type WHERE name = 'super_user';

    -- Get the "TI Department ARG" scope ID
    SELECT scopeId INTO ti_department_arg_scope_id FROM scope WHERE name = 'TI Department ARG';

    -- Check and insert the "super_user" role linked to the "super_user" type and "TI Department ARG" scope
    IF NOT EXISTS (SELECT 1 FROM role WHERE name = 'super_user' AND typeId = super_user_type_id AND scopeId = ti_department_arg_scope_id) THEN
        INSERT INTO role (name, description, typeId, scopeId)
        VALUES ('super_user', 'Super User Role with all permissions in TI Department ARG', super_user_type_id, ti_department_arg_scope_id)
        RETURNING roleId INTO super_user_role_id;
    ELSE
        -- Get the existing "super_user" role ID
        SELECT roleId INTO super_user_role_id FROM role WHERE name = 'super_user' AND typeId = super_user_type_id AND scopeId = ti_department_arg_scope_id;
    END IF;

    -- Step 2: Assign the "super_user" role to the user "juandavidarguello@gmail.com"
    IF NOT EXISTS (SELECT 1 FROM user_role WHERE userId = user_id AND roleId = super_user_role_id) THEN
        INSERT INTO user_role (userId, roleId) VALUES (user_id, super_user_role_id);
    END IF;
END $$;

