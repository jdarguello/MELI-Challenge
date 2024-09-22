-- Insert the basic CRUD permissions if they do not already exist
DO $$
BEGIN
    -- Check and insert "Create" permission
    IF NOT EXISTS (SELECT 1 FROM permission WHERE kind = 'Create') THEN
        INSERT INTO permission (kind) VALUES ('Create');
    END IF;

    -- Check and insert "Update" permission
    IF NOT EXISTS (SELECT 1 FROM permission WHERE kind = 'Update') THEN
        INSERT INTO permission (kind) VALUES ('Update');
    END IF;

    -- Check and insert "Read" permission
    IF NOT EXISTS (SELECT 1 FROM permission WHERE kind = 'Read') THEN
        INSERT INTO permission (kind) VALUES ('Read');
    END IF;

    -- Check and insert "Delete" permission
    IF NOT EXISTS (SELECT 1 FROM permission WHERE kind = 'Delete') THEN
        INSERT INTO permission (kind) VALUES ('Delete');
    END IF;
END $$;

-- Insert the default Type objects if they do not already exist
DO $$
DECLARE
    type_full_stack_id INTEGER;
    type_backend_dev_id INTEGER;
    create_permission_id INTEGER;
    read_permission_id INTEGER;
BEGIN
    -- Get the permission ids for Create and Read
    SELECT permissionId INTO create_permission_id FROM permission WHERE kind = 'Create';
    SELECT permissionId INTO read_permission_id FROM permission WHERE kind = 'Read';

    -- Check and insert "full-stack" type
    IF NOT EXISTS (SELECT 1 FROM type WHERE name = 'full-stack') THEN
        INSERT INTO type (name, description, weight) 
        VALUES ('full-stack', 'full-stack developer', 100)
        RETURNING typeId INTO type_full_stack_id;

        -- Associate permissions "Create" and "Read" with the "full-stack" type
        INSERT INTO type_permission (typeId, permissionId) VALUES (type_full_stack_id, create_permission_id);
        INSERT INTO type_permission (typeId, permissionId) VALUES (type_full_stack_id, read_permission_id);
    ELSE
        -- Get existing typeId if it already exists
        SELECT typeId INTO type_full_stack_id FROM type WHERE name = 'full-stack';
    END IF;

    -- Check and insert "backend-dev" type
    IF NOT EXISTS (SELECT 1 FROM type WHERE name = 'backend-dev') THEN
        INSERT INTO type (name, description, weight)
        VALUES ('backend-dev', 'backend developer', 50)
        RETURNING typeId INTO type_backend_dev_id;

        -- Associate permission "Read" with the "backend-dev" type
        INSERT INTO type_permission (typeId, permissionId) VALUES (type_backend_dev_id, read_permission_id);
    ELSE
        -- Get existing typeId if it already exists
        SELECT typeId INTO type_backend_dev_id FROM type WHERE name = 'backend-dev';
    END IF;
END $$;

-- Insert the default Scope objects if they do not already exist
DO $$
BEGIN
    -- Check and insert "Finance Department COL" scope
    IF NOT EXISTS (SELECT 1 FROM scope WHERE name = 'Finance Department COL') THEN
        INSERT INTO scope (name, description)
        VALUES ('Finance Department COL', 'Financial Services Department in Colombia');
    END IF;

    -- Check and insert "TI Department ARG" scope
    IF NOT EXISTS (SELECT 1 FROM scope WHERE name = 'TI Department ARG') THEN
        INSERT INTO scope (name, description)
        VALUES ('TI Department ARG', 'Technological Services Department in Argentina');
    END IF;
END $$;

-- Insert the default Role objects if they do not already exist
DO $$
DECLARE
    scope_ti_arg_id INTEGER;
    scope_finance_col_id INTEGER;
    type_full_stack_id INTEGER;
    type_backend_dev_id INTEGER;
    role_id INTEGER;
BEGIN
    -- Retrieve the scope IDs
    SELECT scopeId INTO scope_ti_arg_id FROM scope WHERE name = 'TI Department ARG';
    SELECT scopeId INTO scope_finance_col_id FROM scope WHERE name = 'Finance Department COL';

    -- Retrieve the type IDs
    SELECT typeId INTO type_full_stack_id FROM type WHERE name = 'full-stack';
    SELECT typeId INTO type_backend_dev_id FROM type WHERE name = 'backend-dev';

    -- Check and insert "full-stack TI" role
    IF NOT EXISTS (SELECT 1 FROM role WHERE name = 'full-stack TI') THEN
        INSERT INTO role (name, description, typeId, scopeId)
        VALUES ('full-stack TI', 'Full-stack developer for TI department in Argentina', type_full_stack_id, scope_ti_arg_id);
    END IF;

    -- Check and insert "backend-dev Finance" role
    IF NOT EXISTS (SELECT 1 FROM role WHERE name = 'backend-dev Finance') THEN
        INSERT INTO role (name, description, typeId, scopeId)
        VALUES ('backend-dev Finance', 'Backend developer for Finance department in Colombia', type_backend_dev_id, scope_finance_col_id);
    END IF;
END $$;
