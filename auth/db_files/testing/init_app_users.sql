-- Insert the default User objects if they do not already exist
DO $$
DECLARE
    user_id_1 INTEGER;
    user_id_2 INTEGER;
    google_idp_id INTEGER;
    github_idp_id INTEGER;
    role_full_stack_ti_id INTEGER;
    role_backend_finance_id INTEGER;
BEGIN
    -- Get the identity provider IDs for Google and GitHub
    SELECT identityProviderId INTO google_idp_id FROM identity_provider WHERE name = 'Google';
    SELECT identityProviderId INTO github_idp_id FROM identity_provider WHERE name = 'GitHub';

    -- Get the role IDs for "full-stack TI" and "backend-dev Finance"
    SELECT roleId INTO role_full_stack_ti_id FROM role WHERE name = 'full-stack TI';
    SELECT roleId INTO role_backend_finance_id FROM role WHERE name = 'backend-dev Finance';

    -- Check and insert the first user "juandavidarguello@gmail.com"
    IF NOT EXISTS (SELECT 1 FROM app_user WHERE username = 'juandavidarguello@gmail.com') THEN
        INSERT INTO app_user (username, token, tokenExpiryStart, identityProviderId)
        VALUES ('juandavidarguello@gmail.com', '1j3h4h4', CURRENT_DATE, google_idp_id)
        RETURNING userId INTO user_id_1;
        
        -- Assign roles to the first user
        INSERT INTO user_role (userId, roleId) VALUES (user_id_1, role_full_stack_ti_id);
        INSERT INTO user_role (userId, roleId) VALUES (user_id_1, role_backend_finance_id);
    END IF;

    -- Check and insert the second user "jdarguello"
    IF NOT EXISTS (SELECT 1 FROM app_user WHERE username = 'jdarguello') THEN
        INSERT INTO app_user (username, token, tokenExpiryStart, identityProviderId)
        VALUES ('jdarguello', '1j3h4h4', CURRENT_DATE, github_idp_id)
        RETURNING userId INTO user_id_2;

        -- Assign role to the second user
        INSERT INTO user_role (userId, roleId) VALUES (user_id_2, role_backend_finance_id);
    END IF;
END $$;

