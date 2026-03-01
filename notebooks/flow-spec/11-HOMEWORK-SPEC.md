# HOMEWORK SOLVER Feature Specification (v5.0)

> Giải pháp hỗ trợ giải bài tập chi tiết và giải thích logic.
> Áp dụng cơ chế Chain-of-Thought (CoT).

---

## 1. TỔNG QUAN

### Mô tả
Tính năng cho phép người dùng nhập đề bài (Toán, Lý, Hóa...) hoặc chụp ảnh đề bài (sẽ được OCR). AI sẽ giải thích và đưa ra đáp số từng bước.

### Business Rules
- AI không giải đề cho người dùng (No cheating), AI giúp người dùng HIỂU cách giải.
- Phải có giải thích các bước logic (Solving Steps).
- Lưu lịch sử lời giải cho từng người dùng.

---

## 2. API ENDPOINTS

### 2.1 Solve Homework
**Endpoint**: `POST /api/v1/ai/solve-homework`
**Request Body**:
```json
{
  "problem_text": "Tính diện tích hình tròn có bán kính r=5cm",
  "subject": "Math",
  "image_url": "Optional (URL của ảnh chụp đề)"
}
```

**Success Response**:
```json
{
  "id": "uuid-solve-1",
  "problem_text": "Tính diện tích hình tròn có bán kính r=5cm",
  "solution_steps": [
    {
      "step": 1,
      "content": "Xác định công thức diện tích hình tròn: S = π * r^2"
    },
    {
      "step": 2,
      "content": "Thay r = 5 vào công thức: S = π * 5^2"
    },
    {
      "step": 3,
      "content": "Tính toán: S = 25π ≈ 78.54 cm^2"
    }
  ],
  "final_answer": "78.54 cm²",
  "subject": "Math"
}
```

---

## 3. FRONTEND UI FLOW

### Màn hình Giải bài tập (Homework Hub)
- **Input Area**: Textarea cho phép nhập đề bài (hoặc nút Upload ảnh).
- **Selector**: Chọn môn học (Toán, Lý, Hóa, Anh...).
- **Result Area**: Hiển thị lời giải theo Card dạng Timeline (Step 1, Step 2...).
- **Ask AI**: Nút "Hỏi thêm về bước này" (Mở Chat AI với context bước giải đó).

### Luồng tương tác
1. User nhập đề tài.
2. AI loading (với micro-animation "Đang suy luận logic...").
3. Hiển thị từng bước giải (Streaming content).
4. User đánh giá mức độ dễ hiểu của lời giải.

---

*Version: 5.0 - Updated: 2026-03-01*
