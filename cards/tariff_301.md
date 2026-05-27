# 中美贸易摩擦 301 关税清单

## 政策事实

2018 年以后，美国贸易代表办公室围绕 Section 301 对中国相关产品发布多轮加征关税清单。该政策冲击落在 HS 产品层面，适合进一步映射到企业出口结构。

## 适合研究的问题

适合研究出口冲击、市场替代、供应链重组、企业创新、就业调整和融资约束。

## 处理变量如何定义

如果企业 $i$ 在政策前出口多个产品，可以构造企业关税暴露度：

$$
\operatorname{Exposure}_{i}=\sum_{p} s_{ip,0}\operatorname{Tariff}_{p}
$$

其中，$s_{ip,0}$ 是企业 $i$ 在政策前产品 $p$ 的出口份额，$\operatorname{Tariff}_{p}$ 是产品 $p$ 面临的新增关税税率或是否进入清单。

基本模型可以写成：

$$
Y_{it}=\alpha+\beta(\operatorname{Exposure}_{i}\times \operatorname{Post}_{t})+X_{it}'\gamma+\mu_{i}+\lambda_{t}+\varepsilon_{it}
$$

## 数据接口

可连接中国海关数据库、工业企业数据库、上市公司数据、专利数据、USTR 产品清单、UN Comtrade 或 BACI 数据。关键合并键是 HS 产品编码和企业标识。

## 识别风险

高美国市场依赖企业本来就可能与低美国市场依赖企业不同。建议使用政策前出口结构构造权重，控制行业-年份固定效应，并检查政策前趋势。

## 官方来源

- USTR Section 301 Tariff Actions: <https://ustr.gov/issue-areas/enforcement/section-301-investigations/tariff-actions>
