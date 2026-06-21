# collision.py
"""
Xử lý va chạm giữa đạn và các đối tượng trong game.

Hàm chính:
    handle_bullet_collisions(bullets, tanks)
        → Gọi mỗi frame sau khi tất cả bullet.update() đã chạy.
        → Trả về set các tank bị tiêu diệt (để game xử lý thêm).
"""


def handle_bullet_collisions(bullets: list, tanks: list) -> set:
    """
    Kiểm tra từng đạn có trúng tank nào không.

    Quy tắc:
    - Đạn không thể trúng chính tank đã bắn ra nó (owner).
    - Khi trúng: đạn bị hủy (alive = False), tank bị đánh dấu destroyed.
    - Hai đạn đi ngược chiều có thể triệt tiêu nhau.

    Tham số:
        bullets : list[Bullet]  — danh sách đạn hiện có
        tanks   : list[Tank]    — tất cả tank (player + enemy)

    Trả về:
        destroyed : set[Tank]   — các tank bị tiêu diệt lần này
    """
    destroyed = set()

    for bullet in bullets:
        if not bullet.alive:
            continue

        for tank in tanks:
            # Không tự bắn mình
            if tank is bullet.owner:
                continue

            # Va chạm AABB — dùng rect của bullet và rect của tank
            bx = bullet.x - 3   # BULLET_SIZE // 2
            by = bullet.y - 3
            bw = bh = 6

            tx = tank.x
            ty = tank.y
            ts = tank.size

            if (bx < tx + ts and bx + bw > tx and
                    by < ty + ts and by + bh > ty):
                bullet.alive = False
                destroyed.add(tank)

    # Đạn bắn nhau — kiểm tra từng cặp
    for i in range(len(bullets)):
        for j in range(i + 1, len(bullets)):
            b1, b2 = bullets[i], bullets[j]
            if not b1.alive or not b2.alive:
                continue
            # Nếu hai đạn cùng vị trí (sai số 8px)
            if abs(b1.x - b2.x) < 8 and abs(b1.y - b2.y) < 8:
                b1.alive = False
                b2.alive = False

    return destroyed
