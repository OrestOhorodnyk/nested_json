Given the transactions table and table containing exchange rates. Exchange rate timestamps are rounded to second, transaction timestamps are rounded up to the millisecond. We have only data for one day, 1st of April, 2018. Please note there are no exchange rates from GBP to GBP as it is always 1

1) Write down a query that gives us a breakdown of spend in GBP by each user. Use the exchange rate with the largest timestamp. 

INSERT INTO exchange_rates VALUES 
            ( Now(), 'GBP', 'GBP', '1');

-- if it is not alloved to insert row to the the COALESCE may be used

SELECT    user_id, 
          SUM((t.amount * er.rate)) AS total_spent_gbp 
FROM      transactions t 
LEFT JOIN 
          ( 
                   SELECT   from_currency, 
                            to_currency, 
                            (max(array[Extract('EPOCH' FROM ts), rate]))[2] AS rate 
                   FROM     exchange_rates 
                   WHERE    to_currency != 'HUF' 
                   GROUP BY from_currency, 
                            to_currency) AS er 
ON        t.currency = er.from_currency 
GROUP BY  user_id 
ORDER BY  user_id;

DELETE FROM exchange_rates er 
WHERE  er.from_currency = 'GBP' 
       AND er.to_currency = 'GBP'; 

2) Write down the same query, but this time, use the latest exchange rate smaller or equal then the transaction timestamp. The solution should have the two columns: user_id, total_spent_gbp, ordered by user_id


INSERT INTO exchange_rates VALUES 
            ( Now(), 'GBP', 'GBP', '1');

CREATE extension if not exists btree_gist;

DROP INDEX IF EXISTS transactions_ts_index;
CREATE INDEX transactions_ts_index ON transactions USING  gist(ts);


DROP INDEX IF EXISTS exchange_rates_ts_index;
CREATE INDEX exchange_rates_ts_index ON exchange_rates USING  gist(ts);


SELECT     t.user_id, 
           Sum((t.amount * e.rate)) AS total_spent_gbp 
FROM       transactions t 
CROSS JOIN lateral 
           ( 
                    select   er.rate 
                    FROM     exchange_rates er 
                    WHERE    er.to_currency <> 'HUF' 
                    AND      er.from_currency = t.currency 
                    AND      t.ts >= er.ts 
                    ORDER BY er.ts<->t.ts limit 1 ) AS e 
GROUP BY   t.user_id 
ORDER BY   t.user_id;

DELETE FROM exchange_rates er 
WHERE  er.from_currency = 'GBP' 
       AND er.to_currency = 'GBP'; 


-- TASK DESCRIPTION
-- Given the transactions table and table containing exchange rates:

-- 1. Write down a query that gives us a breakdown of spend in GBP by each user.
-- Use the exchange rate with largest timestamp less or equal then transaction timestamp.

-- explain analyze

drop table if exists exchange_rates;
create table exchange_rates(
ts timestamp without time zone,
from_currency varchar(3),
to_currency varchar(3),
rate numeric
);

truncate table exchange_rates;
insert into exchange_rates
values
('2018-04-01 00:00:00', 'USD', 'GBP', '0.71'),
('2018-04-01 00:00:05', 'USD', 'GBP', '0.82'),
('2018-04-01 00:01:00', 'USD', 'GBP', '0.92'),
('2018-04-01 01:02:00', 'USD', 'GBP', '0.62'),

('2018-04-01 02:00:00', 'USD', 'GBP', '0.71'),
('2018-04-01 03:00:05', 'USD', 'GBP', '0.82'),
('2018-04-01 04:01:00', 'USD', 'GBP', '0.92'),
('2018-04-01 04:22:00', 'USD', 'GBP', '0.62'),

('2018-04-01 00:00:00', 'EUR', 'GBP', '1.71'),
('2018-04-01 01:00:05', 'EUR', 'GBP', '1.82'),
('2018-04-01 01:01:00', 'EUR', 'GBP', '1.92'),
('2018-04-01 01:02:00', 'EUR', 'GBP', '1.62'),

('2018-04-01 02:00:00', 'EUR', 'GBP', '1.71'),
('2018-04-01 03:00:05', 'EUR', 'GBP', '1.82'),
('2018-04-01 04:01:00', 'EUR', 'GBP', '1.92'),
('2018-04-01 05:22:00', 'EUR', 'GBP', '1.62'),

('2018-04-01 05:22:00', 'EUR', 'HUF', '0.062')
;


-- Transactions

drop table if exists transactions;
create table transactions (
ts timestamp without time zone,
user_id int,
currency varchar(3),
amount numeric
);

truncate table transactions;
insert into transactions
values
('2018-04-01 00:00:00', 1, 'EUR', 2.45),
('2018-04-01 01:00:00', 1, 'EUR', 8.45),
('2018-04-01 01:30:00', 1, 'USD', 3.5),
('2018-04-01 20:00:00', 1, 'EUR', 2.45),

('2018-04-01 00:30:00', 2, 'USD', 2.45),
('2018-04-01 01:20:00', 2, 'USD', 0.45),
('2018-04-01 01:40:00', 2, 'USD', 33.5),
('2018-04-01 18:00:00', 2, 'EUR', 12.45),

('2018-04-01 18:01:00', 3, 'GBP', 2),

('2018-04-01 00:01:00', 4, 'USD', 2),
('2018-04-01 00:01:00', 4, 'GBP', 2)
;

-- TASK DESCRIPTION
-- Given the transactions table and table containing exchange rates:

-- 1. Write down a query that gives us a breakdown of spend in GBP by each user.
-- Use the exchange rate with largest timestamp less or equal then transaction timestamp.

-- explain analyze

drop table if exists exchange_rates;
create table exchange_rates(
ts timestamp without time zone,
from_currency varchar(3),
to_currency varchar(3),
rate numeric
);

truncate table exchange_rates;
insert into exchange_rates
values
('2018-04-01 00:00:00', 'USD', 'GBP', '0.71'),
('2018-04-01 00:00:05', 'USD', 'GBP', '0.82'),
('2018-04-01 00:01:00', 'USD', 'GBP', '0.92'),
('2018-04-01 01:02:00', 'USD', 'GBP', '0.62'),

('2018-04-01 02:00:00', 'USD', 'GBP', '0.71'),
('2018-04-01 03:00:05', 'USD', 'GBP', '0.82'),
('2018-04-01 04:01:00', 'USD', 'GBP', '0.92'),
('2018-04-01 04:22:00', 'USD', 'GBP', '0.62'),

('2018-04-01 00:00:00', 'EUR', 'GBP', '1.71'),
('2018-04-01 01:00:05', 'EUR', 'GBP', '1.82'),
('2018-04-01 01:01:00', 'EUR', 'GBP', '1.92'),
('2018-04-01 01:02:00', 'EUR', 'GBP', '1.62'),

('2018-04-01 02:00:00', 'EUR', 'GBP', '1.71'),
('2018-04-01 03:00:05', 'EUR', 'GBP', '1.82'),
('2018-04-01 04:01:00', 'EUR', 'GBP', '1.92'),
('2018-04-01 05:22:00', 'EUR', 'GBP', '1.62'),

('2018-04-01 05:22:00', 'EUR', 'HUF', '0.062')
;

-- For volumes of data close to real, run this:
insert into exchange_rates (
select ts, from_currency, to_currency, rate from (
select date_trunc('second', dd + (random() * 60) * '1 second':: interval) as ts, case when random()*2 < 1 then 'EUR' else 'USD' end as from_currency,
'GBP' as to_currency, (200 * random():: int )/100 as rate
FROM generate_series
        ( '2018-04-01'::timestamp 
        , '2018-04-02'::timestamp
        , '1 minute'::interval) dd
     ) a 
where ts not in (select ts from exchange_rates)
order by ts
)
;

-- Transactions

drop table if exists transactions;
create table transactions (
ts timestamp without time zone,
user_id int,
currency varchar(3),
amount numeric
);

truncate table transactions;
insert into transactions
values
('2018-04-01 00:00:00', 1, 'EUR', 2.45),
('2018-04-01 01:00:00', 1, 'EUR', 8.45),
('2018-04-01 01:30:00', 1, 'USD', 3.5),
('2018-04-01 20:00:00', 1, 'EUR', 2.45),

('2018-04-01 00:30:00', 2, 'USD', 2.45),
('2018-04-01 01:20:00', 2, 'USD', 0.45),
('2018-04-01 01:40:00', 2, 'USD', 33.5),
('2018-04-01 18:00:00', 2, 'EUR', 12.45),

('2018-04-01 18:01:00', 3, 'GBP', 2),

('2018-04-01 00:01:00', 4, 'USD', 2),
('2018-04-01 00:01:00', 4, 'GBP', 2)
;

-- For volumes of data close to real, run this:
insert into transactions (
SELECT dd + (random()*5) * '1 second'::interval as ts, (random() * 1000)::int as user_id,
case when random()*2 < 1 then 'EUR' else 'USD' end as currency,
(random() * 10000) :: int / 100 as amount
FROM generate_series
        ( '2018-04-01'::timestamp 
        , '2018-04-02'::timestamp
        , '1 second'::interval) dd
)        ;

