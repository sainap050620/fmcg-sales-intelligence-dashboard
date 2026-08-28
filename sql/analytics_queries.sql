-- 1. Revenue & Margin Contribution by Sales Channel
SELECT 
    Channel,
    COUNT(TransactionID) AS TotalOrders,
    SUM(UnitsSold) AS UnitsSold,
    ROUND(SUM(NetRevenue), 2) AS NetRevenueEUR,
    ROUND(SUM(GrossMargin), 2) AS GrossMarginEUR,
    ROUND((SUM(GrossMargin) / SUM(NetRevenue)) * 100, 2) AS MarginPct
FROM fact_sales
GROUP BY Channel
ORDER BY NetRevenueEUR DESC;

-- 2. Promotional Lift Analysis by Product Category
SELECT 
    Category,
    ROUND(AVG(CASE WHEN IsPromo = 1 THEN UnitsSold ELSE NULL END), 2) AS AvgUnitsPromo,
    ROUND(AVG(CASE WHEN IsPromo = 0 THEN UnitsSold ELSE NULL END), 2) AS AvgUnitsBase,
    ROUND(
        (AVG(CASE WHEN IsPromo = 1 THEN UnitsSold ELSE NULL END) - 
         AVG(CASE WHEN IsPromo = 0 THEN UnitsSold ELSE NULL END)) / 
         AVG(CASE WHEN IsPromo = 0 THEN UnitsSold ELSE NULL END) * 100, 2
    ) AS PromotionalLiftPct
FROM fact_sales
GROUP BY Category
ORDER BY PromotionalLiftPct DESC;
