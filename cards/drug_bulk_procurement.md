# 国家组织药品集中带量采购

## 政策事实

国家组织药品集中采购试点采用「国家组织、联盟采购、平台操作」的组织形式。试点政策对象落在药品、企业和城市层面。

## 适合研究的问题

适合研究药品价格、市场份额、销售费用、研发投入、仿制药替代、医保基金支出、医院用药结构和医药行业整合。

## 处理变量如何定义

药品层面可以定义：

$$
\operatorname{Included}_{d}=1\{d\ \operatorname{is\ included\ in\ centralized\ procurement}\}
$$

企业-药品层面可以定义：

$$
\operatorname{Winner}_{fd}=1\{f\ \operatorname{wins\ procurement\ for\ drug}\ d\}
$$

如果有药品-城市-时间层面数据，可以使用三重差分：

$$
Y_{dct}=\alpha+\beta(\operatorname{Included}_{d}\times \operatorname{PilotCity}_{c}\times \operatorname{Post}_{t})+\mu_{dc}+\lambda_{ct}+\eta_{dt}+\varepsilon_{dct}
$$

## 数据接口

可连接中选药品、中选企业、中选价格、药品编码、通用名、规格、剂型、上市公司年报、医院药品采购数据和医药销售数据库。

## 识别风险

不能简单把所有医药企业设为处理组。真正受冲击的是特定通用名、特定规格、特定城市和特定企业。

## 官方来源

- 国家医保局: <https://www.nhsa.gov.cn/>
