# AI TUTOR - Technical Dependencies & Installation Guide

> Hướng dẫn cài đặt các thư viện bổ trợ cho từng tính năng cốt lõi.

---

## 1. TỔNG QUAN (Tech Stack)

Hệ thống được xây dựng trên nền tảng **Python 3.12** và **FastAPI**. Dưới đây là các nhóm thư viện cần thiết.

### Core Frameworks
- **FastAPI**: Backend framework.
- **SQLAlchemy (Async)**: Làm việc với Database PostgreSQL.
- **Pydantic**: Validate dữ liệu đầu vào/đầu ra.
- **Alembic**: Quản lý database migrations.

---

## 2. CHI TIẾT THEO TÍNH NĂNG

### 📄 2.1 Xử lý Tài liệu (Document Processing)
Để đọc nội dung từ file PDF, Word, hệ thống cần:
- **`pypdf`**: Thư viện mạnh mẽ để extract text từ PDF.
- **`python-docx`**: Dùng để xử lý các file Microsoft Word (.docx).
- **`aiofiles`**: Xử lý đọc/ghi file bất đồng bộ (Async I/O).

```bash
pip install pypdf python-docx aiofiles
```

### 🧠 2.2 RAG & AI Services (LangChain & Claude)
Đây là "trái tim" của hệ thống, xử lý việc hỏi đáp và sinh nội dung.
- **`langchain`**: Framework chính để kết nối LLM và Vector Database.
- **`langchain-anthropic`**: Client chính thức để gọi Claude 3.5 Sonnet.
- **`chromadb`**: Cơ sở dữ liệu Vector để lưu trữ các "mảnh" (chunks) tài liệu.
- **`sentence-transformers`**: Model chạy local để biến văn bản thành vector (Embedding).

```bash
pip install langchain langchain-anthropic chromadb sentence-transformers
```

### ⏱️ 2.3 Xử lý Tác vụ Ngầm (Background Tasks)
Vì việc upload và AI sinh nội dung mất thời gian, chúng ta cần Queue:
- **`redis`**: Dùng làm Message Broker (nơi chứa hàng đợi).
- **`celery`** hoặc **`python-arq`**: Thư viện quản lý Worker thực hiện task.

```bash
pip install redis arq
```

### 🔐 2.4 Bảo mật & Auth
- **`python-jose`**: Xử lý JWT Token.
- **`passlib[bcrypt]`**: Mã hóa mật khẩu người dùng.

```bash
pip install "python-jose[cryptography]" "passlib[bcrypt]"
```

---

## 3. CÁC BƯỚC CÀI ĐẶT (Step-by-Step)

### Bước 1: Khởi tạo môi trường ảo
```bash
python -m venv venv
source venv/bin/activate  # Trên Linux/Mac
# venv\Scripts\activate   # Trên Windows
```

### Bước 2: Cài đặt tất cả dependency
```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình biến môi trường (.env)
Tạo file `.env` và điền các API Key cần thiết:
```env
ANTHROPIC_API_KEY=your_claude_api_key_here
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379
CHROMA_DB_PATH=./chroma_db
```

### Bước 4: Khởi tạo Database
```bash
alembic upgrade head
```

---

## 💡 LƯU Ý CHO "EM BÉ TẬP CODING"

1. **Về LangChain**: Đây là thư viện rất rộng. Em nên tập trung tìm hiểu `Expression Language (LCEL)` và cách dùng `PromptTemplate` đầu tiên.
2. **Về ChromaDB**: Khi cài đặt trên Linux, đôi khi nó yêu cầu `sqlite3` phiên bản mới. Nếu gặp lỗi, hãy báo anh để anh chỉ cách fix nhé.
3. **Về LLMs**: Luôn dùng các thư viện async (như `langchain-anthropic`) để không làm "treo" server khi AI đang suy nghĩ.

*Version: 5.0 - Tài liệu hướng dẫn cài đặt thư viện.*
