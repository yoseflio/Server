create table users
(
    id       int auto_increment
        primary key,
    name     varchar(200) not null,
    password varchar(200) not null,
    email    varchar(200) not null,
    phone    varchar(200) not null,
    constraint users_email
        unique (email),
    constraint users_id
        unique (id)
);

INSERT INTO project_db.users (id, name, password, email, phone) VALUES (1, 'LiorYosef', '7676', 'lioryosef96@gmail.com', '0546321241');
INSERT INTO project_db.users (id, name, password, email, phone) VALUES (3, 'OmerMor', '1234', 'omermor2@gmail.com', '0544895984');
INSERT INTO project_db.users (id, name, password, email, phone) VALUES (4, 'DorBaznak', '1234', 'Dorbaznak@gmail.com', '0541234567');
INSERT INTO project_db.users (id, name, password, email, phone) VALUES (5, 'Netanel', '2222', 'Netanel@gmail.com', '0587654321');
INSERT INTO project_db.users (id, name, password, email, phone) VALUES (6, 'ella', '1234', 'ella@gmail.com', '054621241');
