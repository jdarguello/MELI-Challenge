-- Insert "Google" identity provider
INSERT INTO identity_provider (clientId, name, clientSecret, tokenValidationUrl, tokenExpiryTime)
VALUES (
    :'GOOGLE_CLIENT_ID',            -- Google client ID
    'Google',
    :'GOOGLE_CLIENT_SECRET',        -- Google client secret
    'https://oauth2.googleapis.com/tokeninfo',  -- Google token validation URL
    36000                           -- Token expiry time in seconds (e.g., 36000 seconds = 10 hours)
);

-- Insert "GitHub" identity provider
INSERT INTO identity_provider (clientId, name, clientSecret, tokenValidationUrl, tokenExpiryTime)
VALUES (
    :'GITHUB_CLIENT_ID',            -- GitHub client ID
    'GitHub',
    :'GITHUB_CLIENT_SECRET',        -- GitHub client secret
    'https://api.github.com/user',  -- GitHub token validation URL
    900                             -- Token expiry time in seconds (e.g., 900 seconds = 15 minutes)
);


