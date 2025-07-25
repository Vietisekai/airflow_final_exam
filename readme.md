
# 🚀 ETL Pipeline với Apache Airflow & Astro CLI

Dự án này sử dụng **Apache Airflow** để thực hiện pipeline ETL từ dữ liệu JSON sang cơ sở dữ liệu PostgreSQL. Hệ thống chạy trong Docker thông qua **Astro CLI**.

## 📦 Yêu cầu hệ thống

Trước khi bắt đầu, hãy đảm bảo bạn đã cài đặt các công cụ sau:

- [Docker](https://www.docker.com/products/docker-desktop/)
- [Astro CLI](https://docs.astronomer.io/astro/install-cli) (Command-line tool để quản lý Airflow)

## 🛠️ Các bước cài đặt và chạy dự án

### 1. Clone và truy cập vào thư mục dự án

```bash
git clone <repo-url>
cd <project-folder>
```

### 2. Khởi chạy môi trường Airflow bằng Astro CLI

```bash
astro dev start
```

Lệnh này sẽ:

- Tạo container Docker chạy Airflow (scheduler, webserver, PostgreSQL, etc.)
- Tự động build project và mount code của bạn vào container

Khi quá trình hoàn tất, bạn có thể truy cập giao diện Airflow tại:

```
http://localhost:8080
```


---

### 3. Cấu hình kết nối cơ sở dữ liệu (Postgres)

Sau khi truy cập Airflow UI:

1. Vào tab **"Admin" > "Connections"**
2. Click vào **"+ Add a new connection"**
3. Tạo một kết nối mới với cấu hình sau:

| Trường            | Giá trị         |
|-------------------|------------------|
| **Conn Id**       | `postgres`       |
| **Conn Type**     | `Postgres`       |
| **Host**          | `postgres`       |
| **Schema**        | `postgres`       |
| **Login**         | `postgres`       |
| **Password**      | `postgres`       |
| **Port**          | `5432`           |


---

### 4. Kích hoạt và chạy các DAG

#### 4.1 DAG tạo bảng

- Truy cập UI Airflow (`http://localhost:8080`)
- Bật DAG `create_table_dag`
- Trigger để chạy DAG

#### 4.2 DAG thực hiện ETL

- Bật DAG `tune_stream_etl`
- Trigger để chạy DAG này sau khi bảng đã được tạo

---

## ✅ Kết quả 

- Dữ liệu từ file JSON sẽ được đọc và chèn vào bảng staging trong PostgreSQL.
- Data quality checks thành công và kết thúc DAG.
