UPDATE Sign
SET nodes = (SELECT CASE
             WHEN Sign.dir = 1 THEN (SELECT NODE_A FROM LINK WHERE LINK.link=Sign.link)
             ELSE                   (SELECT NODE_B FROM LINK WHERE LINK.link=Sign.link)
             END as 'nodes');
