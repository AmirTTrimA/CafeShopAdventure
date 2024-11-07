CREATE TABLE cafe_cafe (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    opening_time TIME NOT NULL,
    closing_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cafe_table (
    id SERIAL PRIMARY KEY,
    cafe_id INTEGER REFERENCES cafe_cafe(id) ON DELETE CASCADE,
    number INTEGER NOT NULL,
    status VARCHAR(20) CHECK (status IN ('A', 'U')) DEFAULT 'A',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customer_customer (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    table_number INTEGER NOT NULL,
    cafe_id INTEGER REFERENCES cafe_cafe(id) ON DELETE CASCADE,
    phone_number VARCHAR(12) UNIQUE,
    points INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu_menuitem (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    points INTEGER DEFAULT 0,
    category_id INTEGER REFERENCES menu_category(id) ON DELETE CASCADE,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE staff_staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(12) UNIQUE NOT NULL,
    role CHAR(1) CHECK (role IN ('M', 'S')),
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password VARCHAR(128) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE
);

CREATE TABLE order_order (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customer_customer(id) ON DELETE SET NULL,
    staff_id INTEGER REFERENCES staff_staff(staff_id) ON DELETE CASCADE,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('Pending', 'Processing', 'Completed', 'Cancelled')) DEFAULT 'Pending',
    table_number VARCHAR(10),
    total_price NUMERIC(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_orderitem (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES order_order(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES menu_menuitem(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 1,
    subtotal NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_orderhistory (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customer_customer(id) ON DELETE CASCADE,
    guest_id VARCHAR(36),
    order_data JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
