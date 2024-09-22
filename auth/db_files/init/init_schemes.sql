CREATE TABLE permission (
    permissionId SERIAL PRIMARY KEY,
    kind VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE type (
    typeId SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    weight INTEGER DEFAULT 1
);

CREATE TABLE type_permission (
    typeId INTEGER NOT NULL,
    permissionId INTEGER NOT NULL,
    PRIMARY KEY (typeId, permissionId),
    FOREIGN KEY (typeId) REFERENCES type(typeId) ON DELETE CASCADE,
    FOREIGN KEY (permissionId) REFERENCES permission(permissionId) ON DELETE CASCADE
);

CREATE TABLE scope (
    scopeId SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE role (
    roleId SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    typeId INTEGER NOT NULL,
    scopeId INTEGER NOT NULL,
    FOREIGN KEY (typeId) REFERENCES type(typeId) ON DELETE CASCADE,
    FOREIGN KEY (scopeId) REFERENCES scope(scopeId) ON DELETE CASCADE
);

CREATE TABLE identity_provider (
    identityProviderId SERIAL PRIMARY KEY,
    clientId VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    clientSecret VARCHAR(255) NOT NULL,
    tokenValidationUrl VARCHAR(255) NOT NULL,
    tokenExpiryTime INTEGER NOT NULL
);

CREATE TABLE app_user (
    userId SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    tokenExpiryStart DATE NOT NULL,
    identityProviderId INTEGER,
    FOREIGN KEY (identityProviderId) REFERENCES identity_provider(identityProviderId)
);

CREATE TABLE user_role (
    userId BIGINT NOT NULL,
    roleId INTEGER NOT NULL,
    PRIMARY KEY (userId, roleId),
    FOREIGN KEY (userId) REFERENCES app_user(userId) ON DELETE CASCADE,
    FOREIGN KEY (roleId) REFERENCES role(roleId) ON DELETE CASCADE
);
