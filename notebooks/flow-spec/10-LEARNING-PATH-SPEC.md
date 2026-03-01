# LEARNING PATH Feature Specification (v5.0)

> Cơ chế sinh lộ trình học tập từ tài liệu và theo dõi tiến độ.
> Áp dụng tiêu chuẩn Bloom's Taxonomy.

---

## 1. TỔNG QUAN

### Mô tả
Tính năng tự động phân tích tài liệu để tạo ra một lộ trình học có cấu trúc, giúp người dùng không bị "ngợp" khi đọc tài liệu dài.

### Business Rules
- Một tài liệu chỉ có tối đa 1 lộ trình học (Learning Path).
- Lộ trình gồm nhiều Giai đoạn (Stages).
- Mỗi Giai đoạn gồm nhiều Bài học (Lessons).
- Người dùng đánh dấu hoàn thành bài học để theo dõi tiến độ (%).

---

## 2. API ENDPOINTS

### 2.1 Get Learning Path
**Endpoint**: `GET /api/v1/documents/:document_id/learning-path`
**Response**:
```json
{
  "id": "uuid-path-1",
  "document_id": "uuid-doc-123",
  "title": "Lộ trình học Python Cơ bản",
  "progress_percentage": 45.5,
  "stages": [
    {
      "id": "uuid-stage-1",
      "title": "Giai đoạn 1: Làm quen",
      "order": 1,
      "lessons": [
        {
          "id": "uuid-lesson-101",
          "title": "Biến và Kiểu dữ liệu",
          "summary": "Cách khai báo biến...",
          "status": "completed"
        }
      ]
    }
  ]
}
```

### 2.2 Update Lesson Progress
**Endpoint**: `PATCH /api/v1/lessons/:lesson_id/progress`
**Request Body**: `{ "status": "completed" }`

---

## 3. FRONTEND UI FLOW

### Màn hình Lộ trình (Learning Path View)
- **Header**: Hiển thị tên tài liệu và Progress Bar tổng thể.
- **Accordion List**: Mỗi Stage là một Accordion. Khi mở ra sẽ thấy danh sách Lesson.
- **Lesson Card**: 
  - Hiển thị tiêu đề, tóm tắt bài học.
  - Nút "Học ngay" (Dẫn đến Chat AI với context bài học đó).
  - Checkbox "Đánh dấu hoàn thành".

### Luồng tương tác
1. User upload tài liệu.
2. User nhấn nút "Sinh lộ trình học".
3. AI hiển thị Outline lộ trình -> User nhấn "Xác nhận".
4. Hệ thống lưu vào DB và hiển thị Dashboard lộ trình.

---

*Version: 5.0 - Updated: 2026-03-01*
