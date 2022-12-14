CREATE TABLE products (
  product_id INT PRIMARY KEY AUTO_INCREMENT,
  product_name VARCHAR(100) NOT NULL,
  product_description VARCHAR(500) NOT NULL,
  image_route VARCHAR(500) NOT NULL,
  product_unit_price INT NOT NULL,
  active BIT DEFAULT 1
);

CREATE TABLE companies (
  company_id INT PRIMARY KEY AUTO_INCREMENT,
  company_name VARCHAR(100) NOT NULL,
  username VARCHAR(20) NOT NULL UNIQUE,
  password VARCHAR(250) NOT NULL
);

CREATE TABLE points (
  invoice_id VARCHAR(50) PRIMARY KEY,
  company_id INT NOT NULL,
  valid_from DATE NOT NULL,
  valid_until DATE NOT NULL,
  awarded_points INT NOT NULL,
  spent_points INT NOT NULL DEFAULT 0,
  CONSTRAINT customer_fk FOREIGN KEY (company_id) REFERENCES companies (company_id)
);

CREATE TABLE addresses (
  address_id INT PRIMARY KEY AUTO_INCREMENT,
  address_line1 VARCHAR(100) NOT NULL,
  address_line2 VARCHAR(100),
  city VARCHAR(50),
  state VARCHAR(50),
  country VARCHAR(50),
  zip_code VARCHAR(50),
  company_id INT,
  CONSTRAINT company_fk FOREIGN KEY (company_id) REFERENCES companies (company_id)
);

CREATE TABLE orders (
  order_id INT PRIMARY KEY AUTO_INCREMENT,
  company_id INT NOT NULL,
  address_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  created_at DATE NOT NULL,
  status VARCHAR(100) NOT NULL,
  CONSTRAINT orders_fk1 FOREIGN KEY (company_id) REFERENCES companies (company_id),
  CONSTRAINT orders_fk2 FOREIGN KEY (product_id) REFERENCES products (product_id),
  CONSTRAINT orders_fk3 FOREIGN KEY (address_id) REFERENCES addresses (address_id)
);