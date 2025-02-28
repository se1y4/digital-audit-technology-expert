--Ведомость за май 2019
SELECT e.EMP_NAME, 
       d.DEP_NAME, 
       e.POSITION_, 
       s.AMOUNT AS MAY_SALARY
FROM SALARY s
JOIN EMPLOYER e ON s.EMP_ID_PK = e.EMP_ID_PK
LEFT JOIN DEPARTMENT d ON e.DEP_ID_FK = d.DEP_ID_PK
WHERE s.PERIOD_PK = '2019-05-01';

--Разница между двумя запросами
    --Запрос 1 (с подзапросом)
SELECT e.EMP_NAME,
       (SELECT dep_name FROM department d WHERE d.DEP_ID_PK = e.DEP_ID_FK) dep_name,
       e.POSITION_
FROM EMPLOYER e;

    --Запрос 2 (с JOIN)
SELECT e.EMP_NAME, 
       d.DEP_NAME, 
       e.POSITION_
FROM EMPLOYER e, DEPARTMENT d
WHERE d.DEP_ID_PK = e.DEP_ID_FK;

--Исправленный запрос
SELECT e.EMP_NAME, 
       d.DEP_NAME, 
       e.POSITION_
FROM EMPLOYER e
LEFT JOIN DEPARTMENT d ON e.DEP_ID_FK = d.DEP_ID_PK;

--Список сотрудников, заработавших за 1-й квартал более 2000
SELECT e.EMP_NAME, 
       SUM(s.AMOUNT) AS TOTAL_EARNINGS
FROM SALARY s
JOIN EMPLOYER e ON s.EMP_ID_PK = e.EMP_ID_PK
WHERE s.PERIOD_PK BETWEEN '2019-01-01' AND '2019-03-01'
GROUP BY e.EMP_NAME
HAVING SUM(s.AMOUNT) > 2000;

--Доход сотрудников за год нарастающим итогом
    --Оконная функция
SELECT s.EMP_ID_PK, 
       e.EMP_NAME, 
       s.PERIOD_PK, 
       s.AMOUNT, 
       SUM(s.AMOUNT) OVER (PARTITION BY s.EMP_ID_PK ORDER BY s.PERIOD_PK) AS CUMULATIVE_EARNINGS
FROM SALARY s
JOIN EMPLOYER e ON s.EMP_ID_PK = e.EMP_ID_PK
ORDER BY s.EMP_ID_PK, s.PERIOD_PK;

    --Подзапрос
SELECT s1.EMP_ID_PK, 
       e.EMP_NAME, 
       s1.PERIOD_PK, 
       s1.AMOUNT, 
       (SELECT SUM(s2.AMOUNT) 
        FROM SALARY s2 
        WHERE s2.EMP_ID_PK = s1.EMP_ID_PK 
          AND s2.PERIOD_PK <= s1.PERIOD_PK) AS CUMULATIVE_EARNINGS
FROM SALARY s1
JOIN EMPLOYER e ON s1.EMP_ID_PK = e.EMP_ID_PK
ORDER BY s1.EMP_ID_PK, s1.PERIOD_PK;

--Для ведомости за май 2019 используем JOIN с фильтром по дате.
--Разница между запросами через LEFT JOIN.
--Для поиска сотрудников, заработавших >2000 за 1-й квартал, используем SUM() и HAVING.
--Для годового дохода нарастающим итогом лучше использовать оконную функцию (SUM() OVER()), так как она эффективнее, чем подзапрос.