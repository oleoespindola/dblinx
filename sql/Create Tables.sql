CREATE TABLE dblinx.regional (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    active TINYINT(1) DEFAULT 1
);

ALTER TABLE dblinx.regional 
ADD COLUMN supervisor char(100) not null;

ALTER TABLE dblinx.regional 
ADD COLUMN supervisor_email char(100) not null;

CREATE TABLE dblinx.stores (
    id serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    store_registration VARCHAR(50) UNIQUE NOT NULL,
    store_email VARCHAR(100),
    active BOOL DEFAULT 0,
    regional_id INT NOT NULL
);

ALTER TABLE dblinx.`stores`
ADD CONSTRAINT `fk_regional_id` FOREIGN KEY (`regional_id`) REFERENCES regional (id);

CREATE TABLE dblinx.`employees` (
  `id` int(11) NOT NULL, -- original: vendedor_id
  `name` text NOT NULL, -- original: nome_vendedor
  `admission_date` date DEFAULT NULL, -- original: admissao
  `active` char(3) DEFAULT NULL, -- original: ativo
  `phone` int(11) DEFAULT NULL, -- original: celular
  `cpf` bigint(20) DEFAULT NULL, -- original: cpf
  `termination_date` date DEFAULT NULL, -- original: demissao
  `email` text DEFAULT NULL, -- original: email_vendedor
  `store_id` int(11) DEFAULT NULL, -- original: loja_id
  `display_name` text DEFAULT NULL, -- original: nome_exibicao
  `notes` text DEFAULT NULL, -- original: observacoes
  `professional_whatsapp` bigint(20) DEFAULT NULL, -- original: whatsapp_profissional
  PRIMARY KEY (`id`)
) 

CREATE TABLE dblinx.`product_colors` (
  `id` int(11) NOT NULL, -- original: cor_id
  `description` text DEFAULT NULL, -- original: cor_desricao
  PRIMARY KEY (`id`)
) 

CREATE TABLE dblinx.`product_sectors` (
  `id` int(11) NOT NULL, -- original: setor_id
  `description` text NOT NULL, -- original: setor_desricao
  PRIMARY KEY (`id`)
) 

CREATE TABLE dblinx.`product_brands` (
  `id` int(11) NOT NULL, -- original: marca_id
  `description` text NOT NULL, -- original: marca_desricao
  PRIMARY KEY (`id`)
) 

CREATE TABLE dblinx.`products_registration` (
  `id` INT(11) NOT NULL, -- original: -- produto_id
  `product_active` BOOL default 1, -- original: produto_ativo
  `color_id` INT(11) NOT NULL, -- original: cor_id
  `line_id` INT(11) NOT NULL, -- original: linha_id
  `brand_id` INT(11) NOT NULL, -- original: marca_id
  `sector_id` INT(11) NOT NULL, -- original: setor_id
  `registration_date` DATE NOT NULL, -- original: data_cadastro
  `description` TEXT NOT NULL, -- original: descricao
  `full_description` TEXT NOT NULL, -- original: descricao_completa
  `simple_description` TEXT DEFAULT NULL, -- original: descricao_simples
  `storage` INT(11) DEFAULT NULL, -- original: armazenamento
  `ram` INT(11) DEFAULT NULL, -- original: ram
  
  PRIMARY KEY (`id`),
  KEY `color_id_fk` (`color_id`),
  KEY `brand_id_fk` (`brand_id`),
  KEY `sector_id_fk` (`sector_id`),
  
  CONSTRAINT `color_id_fk` FOREIGN KEY (`color_id`) REFERENCES `product_colors` (`id`),
  CONSTRAINT `brand_id_fk` FOREIGN KEY (`brand_id`) REFERENCES `product_brands` (`id`),
  CONSTRAINT `sector_id_fk` FOREIGN KEY (`sector_id`) REFERENCES `product_sectors` (`id`)
);

CREATE TABLE dblinx.`customers` (
  id INT(11) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  cpf int not null
);

CREATE TABLE dblinx.`sales` (
  `id` int NOT NULL, -- original: faturamento_id
  `registration_date` date NOT NULL, -- original: data_de_emissao
  `operation_nature` varchar(50) NOT NULL, -- original: natureza_de_operacao
  `document` bigint(20) NOT NULL, -- original: documento
  `employee_name` varchar(100) NOT NULL, -- original: vendedor
  `customer_code` bigint(20) NOT NULL, -- original: codigo_customere
  `customer_document` bigint(20) NOT NULL, -- original: documento_customere
  `customer_name` varchar(100) NOT NULL, -- original: nome_customere
  `item_quantity` int(11) NOT NULL, -- original: qtde_item
  `store_id` int(11) NOT NULL, -- original: codigo_empresa
  `price_table` varchar(50) NOT NULL, -- original: tabela_preco
  `payment_plan` varchar(50) NOT NULL, -- original: plano_de_pagamento
  `item_value` decimal(10,2) NOT NULL, -- original: valor_item_nf
  `item_discount` decimal(10,2) NOT NULL, -- original: desconto_item
  `discount_percentage` varchar(20) NOT NULL, -- original: desconto_percentil
  `is_canceled` varchar(3) NOT NULL, -- original: cancelada
  `serial` text NOT NULL, -- original: seriais
  `product_id` int(11) NOT NULL, -- original: codigo_produto
  `employee_id` int(11) DEFAULT NULL, -- original: vendedor_id
  PRIMARY KEY (`id`),
  KEY `store_id_fk` (`store_id`),
  KEY `product_id_fk` (`product_id`),
  KEY `employee_id_fk` (`employee_id`),
  CONSTRAINT `store_id_fk` FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`),
  CONSTRAINT `product_id_fk` FOREIGN KEY (`product_id`) REFERENCES `product_colors` (`id`),
  CONSTRAINT `employee_id_fk` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`)
) 

ALTER TABLE dblinx.sales
ADD CONSTRAINT customer_id_fk FOREIGN KEY (customer_id) REFERENCES customers (id);

CREATE TABLE dblinx.`insurance_sales` (
  `id` varchar(30) NOT NULL, -- original: numero_do_bilhete
  `store_id` int(11) NOT NULL, -- original: empresa
  `registration_date` datetime NOT NULL, -- original: data_de_venda_seguro
  `issue_date` datetime NOT NULL, -- original: data_de_emissao
  `adhesion_date` datetime NOT NULL, -- original: data_de_adesao
  `is_canceled` text NOT NULL, -- original: nota_cancelada
  `validity_start_date` datetime NOT NULL, -- original: data_inicio_vigencia
  `validity_end_date` datetime NOT NULL, -- original: data_fim_vigencia
  `premium_value` double NOT NULL, -- original: valor_do_premio
  `is_value` double NOT NULL, -- original: valor_do_is
  `product` text NOT NULL, -- original: produto
  `serial` text NOT NULL, -- original: imei
  `policy` text NOT NULL, -- original: apolice
  `plan_type` int(11) NOT NULL, -- original: tipo_de_plano
  `warranty_time` bigint(20) NOT NULL, -- original: tempo_de_garantia
  `third_party_service` text NOT NULL, -- original: servico_terceiro
  `invoice_number` bigint(20) NOT NULL, -- original: nf
  `invoice_series` bigint(20) NOT NULL, -- original: serienf
  `invoice_date` datetime NOT NULL, -- original: datanf
  `employee_name` text NOT NULL, -- original: vendedor
  `customer_cpf` bigint(20) NOT NULL, -- original: documento_customere
  `employee_id` int(11) DEFAULT NULL, -- original: vendedor_id
  PRIMARY KEY (`id`),
  KEY `store_id_insurance_fk` (`store_id`),
  KEY `employee_id_insurance_fk` (`employee_id`),
  CONSTRAINT `store_id_insurance_fk` FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`),
  CONSTRAINT `employee_id_insurance_fk` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`)
); 
    
CREATE TABLE dblinx.`mobile_plans` (
  `id` varchar(40) NOT NULL, -- original: sav_id
  `order_date` datetime NOT NULL, -- original: data_pedido
  `order_time` varchar(6) DEFAULT NULL, -- original: hora_pedido
  `operator` text DEFAULT NULL, -- original: operadora
  `plan_name` text DEFAULT NULL, -- original: nome_plano
  `value` decimal(10,2) DEFAULT NULL, -- original: valor
  `payment_method` text DEFAULT NULL, -- original: forma_pagamento
  `sales_method` text DEFAULT NULL, -- original: forma_fatura
  `customer_name` text DEFAULT NULL, -- original: customere_nome
  `customer_cpf` bigint(20) DEFAULT NULL, -- original: customere_cpf
  `customer_email` text DEFAULT NULL, -- original: customere_email
  `employee_name` text DEFAULT NULL, -- original: vendedor_nome
  `employee_cpf` bigint(20) DEFAULT NULL, -- original: vendedor_cpf
  `promoter_cpf` double DEFAULT NULL, -- original: promotor_cpf
  `pos_name` text DEFAULT NULL, -- original: pdv_nome
  `pos_business_name` text DEFAULT NULL, -- original: pdv_razao_social
  `zip_code` bigint(20) DEFAULT NULL, -- original: cep
  `street` text DEFAULT NULL, -- original: logradouro
  `neighborhood` text DEFAULT NULL, -- original: bairro
  `state` varchar(2) DEFAULT NULL, -- original: UF
  `status_message` text DEFAULT NULL, -- original: status_message
  `external_sale_id` text DEFAULT NULL, -- original: venda_id_externo
  `serial` text DEFAULT NULL, -- original: IMEI
  `device_name` text DEFAULT NULL, -- original: nome_aparelho
  `device_purchase_value` decimal(10,2) DEFAULT NULL, -- original: valor_aparelho_compra
  `device_sale_value` decimal(10,2) DEFAULT NULL, -- original: valor_aparelho_venda
  `subsidy` decimal(10,2) DEFAULT NULL, -- original: subsidio
  `ICCid` text DEFAULT NULL, -- original: ICCid
  `modality` text DEFAULT NULL, -- original: modalidade
  `voice_protocol` bigint(20) DEFAULT NULL, -- original: protocolo_voz
  `line_number` bigint(20) DEFAULT NULL, -- original: numero_linha
  `temporary_number` bigint(20) DEFAULT NULL, -- original: numero_provisorio
  `network_name` text DEFAULT NULL, -- original: nome_rede
  `company_registration` text DEFAULT NULL, -- original: cnpj
  `operator_pdv_code` varchar(30) DEFAULT NULL, -- original: cod_pdv_operadora
  `status` varchar(30) DEFAULT NULL, -- original: status
  `reason` varchar(30) DEFAULT NULL, -- original: motivo
  `plan_type` varchar(30) DEFAULT NULL, -- original: tipo_plano
  `loyalty` varchar(30) DEFAULT NULL, -- original: fidelizacao
  `white_label_plan` varchar(30) DEFAULT NULL, -- original: plano_white_label
  PRIMARY KEY (`id`)
) 
