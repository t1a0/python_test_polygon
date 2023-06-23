CREATE TABLE IF NOT EXISTS warehouse (
	wh_id int PRIMARY KEY NOT null,
	wh_name varchar(255) not null,
	wh_location varchar(255) not null 
);
	
CREATE TABLE IF NOT EXISTS product (
	pd_id int PRIMARY KEY NOT NULL,
	pd_name varchar(255) NOT NULL,
	pd_price decimal(10,2) NOT NULL,
	pd_quantity int NOT NULL,
	pd_wh_id int references warehouse(wh_id)
);

INSERT INTO warehouse VALUES(1, 'Склад компанії "Alpha Light"', 'Київ'),
							 (2, 'Склад компанії "UniBox"', 'Київ'),
							 (3, 'Склад компанії "Sun Box"', 'Одеса');

INSERT INTO product VALUES	(1,'Ноутбук Dell XPS 13', 44999.99, 200),
							(2,'Смартфон iPhone 12 Pro', 38999.99, 500, 2),
							(3,'Телевізор Samsung QLED Q80A', 55999.99, 1),
							(4,'Навушники Sony WH-1000XM4', 6499.99, 540, 3),
							(5,'Фотокамера Canon EOS R6', 84999.99, 210, 3),
							(6,'Ноутбук Lenovo ThinkPad X1 Carbon', 42999.99, 2),
							(7,'Смартфон Samsung Galaxy S21 Ultra', 33999.99, 2),
							(8,'Телевізор LG OLED CX', 49999.99, 59, 1),
							(9,'Навушники Bose QuietComfort 35 II', 7499.99, 3),
							(10,'Фотокамера Nikon Z7 II', 89999.99, 120, 3);


UPDATE product SET pd_price = pd_price * 0.20 WHERE pd_quantity < 150;

DELETE FROM product WHERE pd_wh_id = 2;

CREATE INDEX pd_name_index ON product(pd_name);
