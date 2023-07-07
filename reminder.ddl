create table if not exists schedule(
    id int primary key,
    weekday varchar(50),
    weekday_dt text,
    leading text,
    leading_dl text,
    attendant text,
    attendant_dl text,
    cleaner text,
    cleaner_dl text
);