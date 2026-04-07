from langchain_core.tools import tool

# ============================================================
# MOCK DATA — Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# ============================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_450_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "14:00",
            "arrival": "15:20",
            "price": 2_800_000,
            "class": "business",
        },
        {
            "airline": "VietJet Air",
            "departure": "08:30",
            "arrival": "09:50",
            "price": 890_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "11:00",
            "arrival": "12:20",
            "price": 1_200_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "07:00",
            "arrival": "09:15",
            "price": 2_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "10:00",
            "arrival": "12:15",
            "price": 1_350_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "16:00",
            "arrival": "18:15",
            "price": 1_100_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "08:10",
            "price": 1_600_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "07:30",
            "arrival": "09:40",
            "price": 950_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "12:00",
            "arrival": "14:10",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "18:00",
            "arrival": "20:10",
            "price": 3_200_000,
            "class": "business",
        },
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "09:00",
            "arrival": "10:20",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "13:00",
            "arrival": "14:20",
            "price": 780_000,
            "class": "economy",
        },
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "08:00",
            "arrival": "09:00",
            "price": 1_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "15:00",
            "arrival": "16:00",
            "price": 650_000,
            "class": "economy",
        },
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {
            "name": "Mường Thanh Luxury",
            "stars": 5,
            "price_per_night": 1_800_000,
            "area": "Mỹ Khê",
            "rating": 4.5,
        },
        {
            "name": "Sala Danang Beach",
            "stars": 4,
            "price_per_night": 1_200_000,
            "area": "Mỹ Khê",
            "rating": 4.3,
        },
        {
            "name": "Fivitel Danang",
            "stars": 3,
            "price_per_night": 650_000,
            "area": "Sơn Trà",
            "rating": 4.1,
        },
        {
            "name": "Memory Hostel",
            "stars": 2,
            "price_per_night": 250_000,
            "area": "Hải Châu",
            "rating": 4.6,
        },
        {
            "name": "Christina's Homestay",
            "stars": 2,
            "price_per_night": 350_000,
            "area": "An Thượng",
            "rating": 4.7,
        },
    ],
    "Phú Quốc": [
        {
            "name": "Vinpearl Resort",
            "stars": 5,
            "price_per_night": 3_500_000,
            "area": "Bãi Dài",
            "rating": 4.4,
        },
        {
            "name": "Sol by Meliá",
            "stars": 4,
            "price_per_night": 1_500_000,
            "area": "Bãi Trường",
            "rating": 4.2,
        },
        {
            "name": "Lahana Resort",
            "stars": 3,
            "price_per_night": 800_000,
            "area": "Dương Đông",
            "rating": 4.0,
        },
        {
            "name": "9Station Hostel",
            "stars": 2,
            "price_per_night": 200_000,
            "area": "Dương Đông",
            "rating": 4.5,
        },
    ],
    "Hồ Chí Minh": [
        {
            "name": "Rex Hotel",
            "stars": 5,
            "price_per_night": 2_800_000,
            "area": "Quận 1",
            "rating": 4.3,
        },
        {
            "name": "Liberty Central",
            "stars": 4,
            "price_per_night": 1_400_000,
            "area": "Quận 1",
            "rating": 4.1,
        },
        {
            "name": "Cochin Zen Hotel",
            "stars": 3,
            "price_per_night": 550_000,
            "area": "Quận 3",
            "rating": 4.4,
        },
        {
            "name": "The Common Room",
            "stars": 2,
            "price_per_night": 180_000,
            "area": "Quận 1",
            "rating": 4.6,
        },
    ],
}


def format_price(price):
    """Format price with dot separators and đ symbol"""
    return f"{price:,}".replace(",", ".") + "đ"


# ============================================================
# Tool 1 — search_flights
# ============================================================
@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')

    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    # Try forward route first
    key = (origin, destination)
    if key in FLIGHTS_DB:
        flights = FLIGHTS_DB[key]
    else:
        # Try reverse route
        key = (destination, origin)
        if key in FLIGHTS_DB:
            flights = FLIGHTS_DB[key]
            # Note: This is a simplification - in reality we'd need to invert departure/arrival times
            # For this exercise, we'll just note it's a reverse route
        else:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    # Format the response
    result = f"Các chuyến bay từ {origin} đến {destination}:\n"
    for i, flight in enumerate(flights, 1):
        result += f"{i}. {flight['airline']} - {flight['departure']} → {flight['arrival']} - {format_price(flight['price'])} ({flight['class']})\n"

    return result.strip()


# ============================================================
# Tool 2 — search_hotels
# ============================================================
@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VND), mặc định không giới hạn

    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    if city not in HOTELS_DB:
        return f"Không có thông tin khách sạn tại {city}."

    hotels = HOTELS_DB[city]

    # Filter by price
    filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

    if not filtered_hotels:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {format_price(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."

    # Sort by rating descending
    sorted_hotels = sorted(filtered_hotels, key=lambda x: x["rating"], reverse=True)

    # Format the response
    result = f"Khách sạn tại {city} (dưới {format_price(max_price_per_night)}/đêm, sắp xếp theo rating):\n"
    for i, hotel in enumerate(sorted_hotels, 1):
        result += f"{i}. {hotel['name']} - {hotel['stars']} sao - {format_price(hotel['price_per_night'])}/đêm - {hotel['area']} - Rating: {hotel['rating']}/5\n"

    return result.strip()


# ============================================================
# Tool 3 — calculate_budget
# ============================================================
@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.

    Tham số:
    - total_budget: tổng ngân sách ban đầu (VND)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD:
      'vé_máy_bay:890000,khách_sạn:650000')

    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    # Parse expenses string
    expense_dict = {}
    try:
        if expenses.strip():
            expense_items = expenses.split(",")
            for item in expense_items:
                if ":" in item:
                    key, value = item.split(":", 1)  # Split only on first colon
                    expense_dict[key.strip()] = int(value.strip())
                else:
                    return f"Lỗi định dạng expenses: '{item}'. Định dạng đúng là 'tên:số_tiền' (VD: 'vé_máy_bay:890000')"
        else:
            # No expenses
            expense_dict = {}
    except ValueError as e:
        return f"Lỗi khi parsing expenses: {str(e)}. Đảm bảo các giá trị là số nguyên."

    # Calculate total expenses
    total_expenses = sum(expense_dict.values())
    remaining_budget = total_budget - total_expenses

    # Format the response
    result = "Bảng chi phí:\n"
    for key, value in expense_dict.items():
        # Convert snake_case to Vietnamese-like format for display
        display_name = key.replace("_", " ").title()
        result += f"- {display_name}: {format_price(value)}\n"

    result += f"---\n"
    result += f"Tổng chi: {format_price(total_expenses)}\n"
    result += f"Ngân sách: {format_price(total_budget)}\n"

    if remaining_budget < 0:
        result += (
            f"Vượt ngân sách {format_price(abs(remaining_budget))}! Cần điều chỉnh.\n"
        )
    else:
        result += f"Còn lại: {format_price(remaining_budget)}\n"

    return result.strip()
