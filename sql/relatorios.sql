-- 1. Todos os veículos
SELECT v.id, v.marca, v.modelo, v.ano, v.placa, v.cor, p.nome AS proprietario
FROM alisson.veiculos v
JOIN alisson.pessoas p ON v.proprietario_id = p.id;

-- 2. Todos os veículos por pessoa ordenado por nome
SELECT p.nome, v.marca, v.modelo, v.ano, v.placa
FROM alisson.veiculos v
JOIN alisson.pessoas p ON v.proprietario_id = p.id
ORDER BY p.nome;

-- 3. Quem tem mais veículos (homens ou mulheres)
SELECT
    CASE p.sexo WHEN 'M' THEN 'Masculino' ELSE 'Feminino' END AS sexo,
    COUNT(v.id) AS total_veiculos
FROM alisson.pessoas p
LEFT JOIN alisson.veiculos v ON v.proprietario_id = p.id
GROUP BY p.sexo
ORDER BY total_veiculos DESC;

-- 4. Todas as marcas ordenadas pelo número de veículos
SELECT marca, COUNT(*) AS total
FROM alisson.veiculos
GROUP BY marca
ORDER BY total DESC;

-- 5. Totais de marcas separados entre homens e mulheres
SELECT
    v.marca,
    CASE p.sexo WHEN 'M' THEN 'Masculino' ELSE 'Feminino' END AS sexo,
    COUNT(*) AS total
FROM alisson.veiculos v
JOIN alisson.pessoas p ON v.proprietario_id = p.id
GROUP BY v.marca, p.sexo
ORDER BY v.marca, total DESC;


-- =====================================================
-- RELATÓRIOS DE PESSOAS
-- =====================================================

-- 6. Todas as pessoas
SELECT id, nome, email, cpf, telefone, sexo, data_nascimento
FROM alisson.pessoas
ORDER BY nome;

-- 7. Pessoas separadas por sexo com idade média
SELECT
    CASE sexo WHEN 'M' THEN 'Masculino' ELSE 'Feminino' END AS sexo,
    COUNT(*) AS total,
    ROUND(AVG(EXTRACT(YEAR FROM AGE(data_nascimento))), 1) AS idade_media
FROM alisson.pessoas
GROUP BY sexo;


-- =====================================================
-- RELATÓRIOS DE REVISÕES
-- =====================================================

-- 8. Todas as revisões dentro de um período
SELECT r.id, p.nome, v.marca, v.modelo, v.placa,
       r.data_revisao, r.kilometragem, r.valor, r.oficina, r.descricao
FROM alisson.revisoes r
JOIN alisson.veiculos v ON r.veiculo_id = v.id
JOIN alisson.pessoas p ON v.proprietario_id = p.id
WHERE r.data_revisao BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY r.data_revisao;

-- 9. Marcas com maior número de revisões
SELECT v.marca, COUNT(r.id) AS total_revisoes
FROM alisson.revisoes r
JOIN alisson.veiculos v ON r.veiculo_id = v.id
GROUP BY v.marca
ORDER BY total_revisoes DESC;

-- 10. Pessoas com maior número de revisões
SELECT p.nome, COUNT(r.id) AS total_revisoes
FROM alisson.revisoes r
JOIN alisson.veiculos v ON r.veiculo_id = v.id
JOIN alisson.pessoas p ON v.proprietario_id = p.id
GROUP BY p.nome
ORDER BY total_revisoes DESC;

-- 11. Média de tempo entre revisões por pessoa
SELECT p.nome, ROUND(AVG(diff), 1) AS media_dias_entre_revisoes
FROM (
    SELECT
        v.proprietario_id,
        r.data_revisao - LAG(r.data_revisao) OVER (
            PARTITION BY v.proprietario_id ORDER BY r.data_revisao
        ) AS diff
    FROM alisson.revisoes r
    JOIN alisson.veiculos v ON r.veiculo_id = v.id
) sub
JOIN alisson.pessoas p ON sub.proprietario_id = p.id
WHERE diff IS NOT NULL
GROUP BY p.nome
ORDER BY media_dias_entre_revisoes;

-- 12. Próximas revisões baseado no tempo médio
SELECT
    p.nome,
    v.marca, v.modelo, v.placa,
    MAX(r.data_revisao) AS ultima_revisao,
    AVG(diff)::integer AS media_dias,
    MAX(r.data_revisao) + (AVG(diff)::integer * INTERVAL '1 day') AS proxima_revisao
FROM (
    SELECT
        r.id, r.veiculo_id, r.data_revisao,
        r.data_revisao - LAG(r.data_revisao) OVER (
            PARTITION BY r.veiculo_id ORDER BY r.data_revisao
        ) AS diff
    FROM alisson.revisoes r
) r
JOIN alisson.veiculos v ON r.veiculo_id = v.id
JOIN alisson.pessoas p ON v.proprietario_id = p.id
WHERE diff IS NOT NULL
GROUP BY p.nome, v.marca, v.modelo, v.placa
ORDER BY proxima_revisao;