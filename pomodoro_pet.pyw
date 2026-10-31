"""POMODORO PET - 1 file duy nhất cho Windows.
Chạy: nhấp đúp file này (cần cài Python 3.9+ từ python.org, không cần thư viện nào khác).
Đóng gói thành .exe:  pip install pyinstaller  rồi  pyinstaller --onefile --windowed --name PomodoroPet pomodoro_pet.pyw
Thoát khẩn cấp khi thú cưng đang chặn màn hình: Ctrl + Shift + X
App TỰ ĐO mức tập trung: đọc tên cửa sổ đang dùng, thời gian không thao tác và tần suất chuyển cửa sổ (chỉ trong bộ nhớ, không lưu tiêu đề).
Nếu app có lỗi, chi tiết được ghi vào file .pomodoro_pet.log trong thư mục người dùng.
"""
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog
import csv, json, os, math, random, time, struct, wave, tempfile, threading, ctypes, traceback, unicodedata, re, datetime as dt, queue
try:
    import winsound
except ImportError:
    winsound = None
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

DATA = os.path.join(os.path.expanduser("~"), ".pomodoro_pet.json")
LOGF = os.path.join(os.path.expanduser("~"), ".pomodoro_pet.log")

def log(text=None):
    """Ghi lỗi vào file log (không bao giờ làm app bị đơ)."""
    try:
        if os.path.exists(LOGF) and os.path.getsize(LOGF) > 200000: return
        with open(LOGF, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + (text or traceback.format_exc()) + "\n")
    except Exception:
        pass
KEY, BG, CARD, CHIP, MUTE, ACC, GOLD = "#010203", "#120e26", "#241c47", "#3a2f6b", "#b8aee0", "#ff5c8a", "#ffd98a"
PETS = ["Mèo", "Cún", "Cá", "Chim"]
MUS = [("off", "Tắt"), ("lofi", "Lo-fi"), ("rain", "Mưa"), ("sea", "Sóng biển"), ("file", "File .wav")]
VOLS = {"Nhỏ": .3, "Vừa": .6, "To": 1.0}
PRAISE = ["Tuyệt vời! Bạn tập trung hơn hôm qua rồi đó!", "Ít xao nhãng hơn hôm qua, tiến bộ thấy rõ!", "Giỏi quá, cứ giữ phong độ này nhé!"]
NUDGE = ["Hôm nay hơi xao nhãng hơn hôm qua. Cất điện thoại đi và thử lại nhé!", "Bạn làm được tốt hơn thế mà! Hít thở sâu rồi tập trung lại nào.", "Chưa bằng hôm qua, nhưng vẫn còn cả buổi để bứt lên!"]


# ====================== VẼ THÚ CƯNG (hoạt hình bằng code) ======================
def draw_pet(c, name, x, y, size, t, flip=False):
    k = size / 200.0
    bob = math.sin(t * 2.2) * 2.5
    blink = (t % 4.5) < .14
    ox = oy = 0.0

    def P(a, b):
        a = (200 - a) if flip else a
        return x + (a + ox) * k, y + (b + oy) * k
    def oval(x1, y1, x2, y2, f):
        c.create_oval(*P(x1, y1), *P(x2, y2), fill=f, outline="", tags="pet")
    def poly(pts, f, sm=False):
        c.create_polygon([v for p in pts for v in P(*p)], fill=f, outline="", smooth=sm, tags="pet")
    def line(pts, f, w, sm=True):
        c.create_line([v for p in pts for v in P(*p)], fill=f, width=max(1, w * k), capstyle="round", joinstyle="round", smooth=sm, tags="pet")
    def eyes(x1, x2, cy):
        for ex in (x1, x2):
            if blink:
                line([(ex - 7, cy), (ex + 7, cy)], "#2b2523", 3, False)
            else:
                oval(ex - 7, cy - 9, ex + 7, cy + 9, "#2b2523"); oval(ex - 4, cy - 8, ex + 1, cy - 3, "#ffffff")

    h = bob
    if name == "Mèo":
        w = math.sin(t * 2.4) * 10
        line([(148, 160), (186, 162), (188, 118 + w), (172 + w, 100)], "#e8955a", 16)
        oval(50, 112, 150, 188, "#f4b26e"); oval(74, 140, 126, 184, "#fde3c4")
        oval(61, 175, 91, 193, "#fde3c4"); oval(109, 175, 137, 193, "#fde3c4")
        poly([(56, 78 + h), (60, 28 + h), (96, 52 + h)], "#f4b26e"); poly([(144, 78 + h), (140, 28 + h), (104, 52 + h)], "#f4b26e")
        poly([(64, 66 + h), (66, 42 + h), (84, 54 + h)], "#f7a8b4"); poly([(136, 66 + h), (134, 42 + h), (116, 54 + h)], "#f7a8b4")
        oval(50, 42 + h, 150, 126 + h, "#f4b26e")
        for a, b in (((100, 44), (100, 58)), ((88, 48), (91, 58)), ((112, 48), (109, 58))):
            line([(a[0], a[1] + h), (b[0], b[1] + h)], "#d98040", 5, False)
        eyes(80, 120, 86 + h)
        oval(58, 95 + h, 74, 105 + h, "#f7a8b4"); oval(126, 95 + h, 142, 105 + h, "#f7a8b4")
        poly([(95, 98 + h), (105, 98 + h), (100, 104 + h)], "#e5707f")
        line([(87, 106 + h), (100, 104 + h), (113, 106 + h)], "#2b2523", 2.5)
        for yy, d in ((96, -4), (102, 4)):
            line([(60, yy + h), (36, yy + d + h)], "#ffffff", 2, False); line([(140, yy + h), (164, yy + d + h)], "#ffffff", 2, False)
    elif name == "Cún":
        w = math.sin(t * 14) * 12
        line([(148, 158), (178 + w, 150), (184 + w, 126), (178 + w, 112)], "#b9773f", 16)
        oval(50, 112, 150, 188, "#d79a5b"); oval(74, 140, 126, 184, "#f7e0bf")
        oval(61, 175, 91, 193, "#f7e0bf"); oval(109, 175, 137, 193, "#f7e0bf")
        oval(37, 48 + h, 71, 124 + h, "#8a5428"); oval(129, 48 + h, 163, 124 + h, "#8a5428")
        oval(52, 42 + h, 148, 126 + h, "#d79a5b"); oval(73, 84 + h, 127, 124 + h, "#f7e0bf")
        eyes(79, 121, 80 + h)
        line([(66, 64 + h), (76, 58 + h), (88, 60 + h)], "#8a5428", 4); line([(134, 64 + h), (124, 58 + h), (112, 60 + h)], "#8a5428", 4)
        oval(90, 87 + h, 110, 101 + h, "#2b2523")
        line([(100, 101 + h), (100, 107 + h)], "#2b2523", 2.5, False); line([(85, 109 + h), (100, 107 + h), (115, 109 + h)], "#2b2523", 2.5)
        oval(93, 108 + h, 107, 121 + h + math.sin(t * 9) * 4, "#ef6f86")
    elif name == "Cá":
        ox, oy = math.sin(t * 1.1) * 5, math.sin(t * 1.6) * 6
        w = math.sin(t * 6) * 10
        poly([(142, 100), (190, 64 + w), (182, 100), (190, 136 - w)], "#ff7a3a")
        poly([(78, 66), (104, 28), (132, 70)], "#ff7a3a"); poly([(92, 136), (112, 166), (134, 134)], "#ff7a3a")
        oval(45, 58, 155, 142, "#ffa45c"); oval(58, 100, 134, 136, "#ffe0bd")
        line([(112, 62), (122, 100), (112, 138)], "#ffffff", 7); line([(132, 70), (140, 100), (132, 130)], "#ffffff", 7)
        oval(57, 81, 79, 103, "#ffffff"); oval(59, 86, 71, 98, "#2b2523"); oval(61, 87, 65, 91, "#ffffff")
        line([(50, 112), (58, 117), (66, 112)], "#c4561f", 3)
        for i in range(3):
            ph = (t * .5 + i * .33) % 1; bx, by, r = 40 - i * 10 + math.sin(ph * 6) * 4, 84 - ph * 56, 6 - i
            c.create_oval(*P(bx - r, by - r), *P(bx + r, by + r), outline="#ffffff", width=2, tags="pet")
    else:  # Chim
        f = math.sin(t * 9) * 26
        oy = bob * .6
        poly([(118, 150), (158, 186), (122, 176)], "#3fa0e0")
        oval(44, 56, 156, 168, "#6ec6ff"); oval(66, 102, 134, 162, "#e8f7ff")
        line([(100, 58), (92, 38), (80, 40)], "#3fa0e0", 7); line([(100, 58), (102, 30), (106, 26)], "#3fa0e0", 7); line([(100, 58), (112, 38), (124, 42)], "#3fa0e0", 7)
        eyes(80, 120, 100)
        oval(56, 109, 72, 119, "#ff9db0"); oval(128, 109, 144, 119, "#ff9db0")
        poly([(90, 110), (110, 110), (100, 125)], "#ffb02e")
        poly([(56, 108), (22, 118 + f), (28, 152 + f * .6), (56, 150)], "#3fa0e0", True)
        poly([(144, 108), (178, 118 + f), (172, 152 + f * .6), (144, 150)], "#3fa0e0", True)
        line([(84, 166), (84, 184)], "#ffb02e", 6); line([(116, 166), (116, 184)], "#ffb02e", 6)


def rrect(c, x1, y1, x2, y2, r, **kw):
    pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
    return c.create_polygon(pts, smooth=True, **kw)


def heart(c, x, y, s, col):
    c.create_polygon(x, y + s * .5, x - s * .55, y - s * .05, x - s * .35, y - s * .5, x, y - s * .25, x + s * .35, y - s * .5, x + s * .55, y - s * .05,
                     fill=col, outline="", smooth=True)


# ====================== ÂM THANH (tự tạo, không chặn giao diện) ======================
SR = 11025

def synth(kind, vol):
    """Tạo âm thanh thuần Python. Nhường CPU đều đặn để giao diện không bị đơ."""
    rnd = random.Random(3)
    if kind == "rain":
        n, lp, out = SR * 6, 0.0, []
        for i in range(n):
            if i % 4096 == 0: time.sleep(.0005)
            x = rnd.uniform(-1, 1); lp += .15 * (x - lp); out.append((x - lp) * .55 * vol)
        return out
    if kind == "sea":
        n, b, lp, out = SR * 10, 0.0, 0.0, []
        for i in range(n):
            if i % 4096 == 0: time.sleep(.0005)
            b = (b + .02 * rnd.uniform(-1, 1)) / 1.02; lp += .05 * (b * 3.5 - lp)
            out.append(lp * (.08 + .92 * math.sin(math.pi * i / n) ** 2) * 1.4 * vol)
        return out
    seg = SR * 3; n = seg * 4
    out = [0.0] * n
    chords = [[220, 261.63, 329.63], [174.61, 220, 261.63], [261.63, 329.63, 392], [196, 246.94, 293.66]]
    for kk, ch in enumerate(chords):
        for i in range(seg):
            if i % 4096 == 0: time.sleep(.0005)
            tt, env, s = i / SR, math.sin(math.pi * i / seg) ** 2, 0.0
            for f in ch:
                s += math.sin(6.2832 * f * tt) + .5 * math.sin(3.1416 * f * tt)
            out[kk * seg + i] += s * env * .11 * vol
    for j in range(24):
        if rnd.random() < .6:
            f, st = rnd.choice([440, 523.25, 587.33, 659.25, 783.99]), int(j * SR * .5)
            for i in range(int(SR * 1.2)):
                out[(st + i) % n] += math.sin(6.2832 * f * i / SR) * math.exp(-3.4 * i / SR) * .2 * vol
            time.sleep(.001)
    return out

def write_wav(path, samples):
    ints = [int(max(-1, min(1, v)) * 32000) for v in samples]
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(struct.pack("<%dh" % len(ints), *ints))

def ensure_wav(kind, vol):
    path = os.path.join(tempfile.gettempdir(), f"pomopet_v2_{kind}_{int(vol * 100)}.wav")
    if not os.path.exists(path):
        tmp = path + ".part"
        write_wav(tmp, synth(kind, vol)); os.replace(tmp, path)       # tránh file dở dang
    return path


# ====================== THÀNH PHẦN GIAO DIỆN (tự co giãn theo màn hình) ======================
Z = 1.0                      # hệ số theo độ phân giải màn hình (DPI)
def z(n): return int(n * Z)
def F(size, bold=False): return ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)

def mix(c, t=.15):
    r, g, b = [int(c[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(v + (255 - v) * t) for v in (r, g, b))


class Btn(tk.Canvas):
    """Nút bo tròn, có hiệu ứng khi rê chuột. sel = màu khi được chọn."""
    def __init__(s, p, text, cmd, bg=CHIP, sel=None, size=11, padx=22, pady=10, texts=None, repeat=False, bgp=None):
        s.f = tkfont.Font(family="Segoe UI", size=size, weight="bold")
        s.w = max(s.f.measure(t) for t in (texts or [text])) + z(padx) * 2
        s.h = s.f.metrics("linespace") + z(pady) * 2
        super().__init__(p, width=s.w, height=s.h, bg=bgp or p.cget("bg"), highlightthickness=0, cursor="hand2")
        s.text, s.cmd, s.bgc, s.selc, s.on, s.repeat, s.job, s.hover = text, cmd, bg, sel, False, repeat, None, False
        s.bind("<ButtonPress-1>", s.press); s.bind("<ButtonRelease-1>", s.rel)
        s.bind("<Enter>", lambda e: s.set_hover(True)); s.bind("<Leave>", lambda e: s.set_hover(False))
        s.draw()
    def press(s, e):
        if s.cmd: s.cmd()
        if s.repeat: s.job = s.after(400, s.rep)
    def rep(s):
        if s.cmd: s.cmd()
        s.job = s.after(70, s.rep)
    def rel(s, e):
        if s.job: s.after_cancel(s.job); s.job = None
    def set_hover(s, h): s.hover = h; s.draw()
    def set(s, text=None, on=None):
        if (text is None or text == s.text) and (on is None or on == s.on): return
        if text is not None: s.text = text
        if on is not None: s.on = on
        s.draw()
    def draw(s):
        s.delete("all")
        col = s.selc if (s.on and s.selc) else s.bgc
        rrect(s, 1, 1, s.w - 1, s.h - 1, s.h / 2, fill=mix(col) if s.hover else col, outline="")
        s.create_text(s.w / 2, s.h / 2, text=s.text, fill="#ffffff", font=s.f)


class Flow(tk.Frame):
    """Khung tự xuống dòng khi cửa sổ hẹp."""
    def __init__(s, p, **k):
        super().__init__(p, **k); s.items = []; s.bind("<Configure>", s.relayout)
    def add(s, w): s.items.append(w)
    def relayout(s, e=None):
        W, x, y, rh = s.winfo_width(), 0, 0, 0
        for w in s.items:
            rw, h = w.winfo_reqwidth() + z(6), w.winfo_reqheight() + z(6)
            if x + rw > W and x > 0: x, y, rh = 0, y + rh, 0
            w.place(x=x, y=y); x += rw; rh = max(rh, h)
        if int(float(s.cget("height"))) != y + rh: s.configure(height=y + rh)


class Scroll(tk.Frame):
    def __init__(s, p, bg):
        super().__init__(p, bg=bg)
        s.c = tk.Canvas(s, bg=bg, highlightthickness=0); s.c.pack(fill="both", expand=True)
        s.inner = tk.Frame(s.c, bg=bg); s.win = s.c.create_window(0, 0, window=s.inner, anchor="nw")
        s.c.bind("<Configure>", lambda e: s.c.itemconfigure(s.win, width=e.width))
        s.inner.bind("<Configure>", lambda e: s.c.configure(scrollregion=s.c.bbox("all")))
    def wheel(s, e): s.c.yview_scroll(int(-e.delta / 120), "units")


# ====================== MÀN HÌNH NGHỈ: lớp phủ + thú cưng tự chạy nhảy + nút Thoát ======================
def virtual_screen():
    try:
        u = ctypes.windll.user32
        return u.GetSystemMetrics(76), u.GetSystemMetrics(77), u.GetSystemMetrics(78), u.GetSystemMetrics(79)
    except Exception:
        return 0, 0, None, None

class Overlay:
    """3 cửa sổ nhẹ thay vì 1 cửa sổ toàn màn hình phải vẽ lại liên tục (nguyên nhân gây lag):
       1) lớp mờ phủ kín mọi màn hình (đứng yên, chặn chuột)   2) cửa sổ nhỏ chứa thú cưng (chỉ di chuyển)   3) nút Thoát."""
    def __init__(s, app, pet, strict):
        s.app, s.pet, s.strict, s.alive = app, pet, strict, True
        r = app.root
        s.sw, s.sh = r.winfo_screenwidth(), r.winfo_screenheight()
        vx, vy, vw, vh = virtual_screen(); vw, vh = vw or s.sw, vh or s.sh
        def top(**k):
            w = tk.Toplevel(r); w.overrideredirect(True); w.attributes("-topmost", True); w.configure(**k); return w
        s.dim = top(bg="#120c2d"); s.dim.geometry(f"{vw}x{vh}{vx:+d}{vy:+d}")
        try: s.dim.attributes("-alpha", .55)
        except tk.TclError: pass
        s.size = min(z(300), int(s.sh * .32)); s.wh = int(s.size * 1.4); s.pad = s.wh - s.size     # phần trống phía trên để hiện trái tim
        s.win = top(bg=KEY); s.win.geometry(f"{s.size}x{s.wh}+{s.sw // 2}+{s.sh // 2}")
        try: s.win.attributes("-transparentcolor", KEY)
        except tk.TclError: pass
        s.c = tk.Canvas(s.win, width=s.size, height=s.wh, bg=KEY, highlightthickness=0); s.c.pack()
        s.c.tag_bind("pet", "<Button-1>", s.poke)
        s.bw = None
        if not strict:
            s.bw = top(bg=KEY)
            try: s.bw.attributes("-transparentcolor", KEY)
            except tk.TclError: pass
            b = Btn(s.bw, "Thoát", app.end_break, bg=CARD, size=12, padx=28, pady=10, bgp=KEY); b.pack()
            s.bw.geometry(f"{b.w}x{b.h}+{s.sw - b.w - z(28)}+{z(24)}")
        for w in (s.dim, s.win): w.bind("<Escape>", lambda e: s.esc())
        s.x = s.tx = s.sw / 2 - s.size / 2; s.y = s.ty = s.sh * .3
        s.t0 = s.last = time.time(); s.n, s.next, s.pj, s.state, s.hearts = 0, 0, -9, "rest", []
        try: s.dim.focus_force()
        except Exception: pass
        s.loop()

    def esc(s):
        if not s.strict: s.app.end_break()
    def poke(s, e):
        t = time.time() - s.t0; s.pj = t; s.hearts.append([e.x, e.y, t])
    def close(s):
        s.alive = False
        for w in (s.win, s.dim, s.bw):
            if w is not None:
                try: w.destroy()
                except Exception: pass

    def step(s, t, dt):
        """Thú cưng TỰ chạy nhảy, không phụ thuộc chuột."""
        W, H, sz = s.sw, s.sh, s.size
        moving, flip = False, False
        if s.pet in ("Cá", "Chim"):                       # bay lượn ngẫu nhiên
            if t >= s.next:
                s.tx, s.ty, s.next = random.uniform(0, W - sz), random.uniform(H * .08, H * .6), t + random.uniform(2.5, 5)
            k = min(1.0, dt * 1.1); dx = s.tx - s.x
            s.x += dx * k; s.y += (s.ty - s.y) * k
            moving, flip = abs(dx) > 12, (s.pet == "Cá" and dx > 0)
            y = s.y + math.sin(t * 2.2) * sz * .05
        else:                                             # chạy - nghỉ - nhảy lên
            if s.state == "run" and abs(s.tx - s.x) < 8: s.next = min(s.next, t)
            if t >= s.next:
                if s.state == "run": s.state, s.next = "rest", t + random.uniform(1.2, 2.5)
                else: s.state, s.tx, s.next = "run", random.uniform(0, W - sz), t + random.uniform(3, 6)
                if random.random() < .5: s.pj = t
            dx = s.tx - s.x
            if s.state == "run" and abs(dx) > 8:
                s.x += math.copysign(min(abs(dx), sz * 1.7 * dt), dx); moving = True
            bounce = abs(math.sin(t * 9)) * sz * .22 if moving else 0
            if t - s.pj < .6: bounce += math.sin((t - s.pj) / .6 * math.pi) * sz * .4
            y = H - sz - z(60) - bounce
        s.x = max(0, min(W - sz, s.x))
        return y, flip

    def loop(s):
        if not s.alive: return
        try:
            now = time.time(); dt = min(.1, now - s.last); s.last = now; t = now - s.t0; s.n += 1
            try:   # phím thoát khẩn cấp Ctrl+Shift+X
                g = ctypes.windll.user32.GetAsyncKeyState
                if g(0x11) & 0x8000 and g(0x10) & 0x8000 and g(0x58) & 0x8000:
                    s.app.end_break(); return
            except Exception: pass
            if s.n % 60 == 0:
                s.dim.lift(); s.win.lift()
                if s.bw is not None: s.bw.lift()
            y, flip = s.step(t, dt)
            c = s.c; c.delete("all")
            draw_pet(c, s.pet, 0, s.pad, s.size, t, flip)
            s.hearts = [h for h in s.hearts if t - h[2] < 1.2]
            for h in s.hearts: heart(c, h[0], h[1] - (t - h[2]) * 70, 18 + (t - h[2]) * 14, ACC)
            s.win.geometry(f"+{int(s.x)}+{int(y - s.pad)}")
        except Exception:
            log()
        finally:
            if s.alive: s.win.after(33, s.loop)


# ====================== KHAY HỆ THỐNG (cạnh đồng hồ Windows) ======================
try:
    from ctypes import wintypes as wt
    LRESULT = ctypes.c_ssize_t
    WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM)
    class WNDCLASS(ctypes.Structure):
        _fields_ = [("style", wt.UINT), ("lpfnWndProc", WNDPROC), ("cbClsExtra", ctypes.c_int), ("cbWndExtra", ctypes.c_int),
                    ("hInstance", wt.HINSTANCE), ("hIcon", wt.HICON), ("hCursor", wt.HANDLE), ("hbrBackground", wt.HBRUSH),
                    ("lpszMenuName", wt.LPCWSTR), ("lpszClassName", wt.LPCWSTR)]
    class NID(ctypes.Structure):
        _fields_ = [("cbSize", wt.DWORD), ("hWnd", wt.HWND), ("uID", wt.UINT), ("uFlags", wt.UINT), ("uCallbackMessage", wt.UINT),
                    ("hIcon", wt.HICON), ("szTip", wt.WCHAR * 128), ("dwState", wt.DWORD), ("dwStateMask", wt.DWORD),
                    ("szInfo", wt.WCHAR * 256), ("uVersion", wt.UINT), ("szInfoTitle", wt.WCHAR * 64), ("dwInfoFlags", wt.DWORD),
                    ("guidItem", ctypes.c_byte * 16), ("hBalloonIcon", wt.HICON)]
    class PT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    HAS_TRAY = True
except Exception:
    HAS_TRAY = False


def make_ico(path):
    """Vẽ biểu tượng quả cà chua 32x32 và lưu thành file .ico."""
    n, px = 32, []
    for y in range(n):
        for x in range(n):
            dx, dy = x + .5 - 16, y + .5 - 19
            a = max(0.0, min(1.0, 14 - math.hypot(dx, dy) + .5))
            col = [0xe8, 0x55, 0x4e]
            hl = max(0.0, 1 - math.hypot(x + .5 - 11, y + .5 - 14) / 4.5)
            col = [int(c + (255 - c) * hl * .55) for c in col]
            if abs(x + .5 - 16) / 7 + abs(y + .5 - 7) / 3.6 <= 1 or (15 <= x <= 16 and 2 <= y <= 6):
                col, a = [0x3a, 0x9d, 0x5d], 1.0
            px.append((col[2], col[1], col[0], int(a * 255)))          # B, G, R, A
    xor = b"".join(bytes(px[y * n + x]) for y in range(n - 1, -1, -1) for x in range(n))
    data = struct.pack("<IiiHHIIiiII", 40, n, n * 2, 1, 32, 0, len(xor) + 4 * n, 0, 0, 0, 0) + xor + bytes(4 * n)
    with open(path, "wb") as f:
        f.write(struct.pack("<HHH", 0, 1, 1) + struct.pack("<BBBBHHII", n, n, 0, 0, 1, 32, len(data), 22) + data)


class Tray:
    CB = 0x8001
    def __init__(s, app):
        s.app, s.ok, s.tip, s.hwnd = app, False, "", None
        s.events = queue.SimpleQueue()
        if not HAS_TRAY: return
        try:
            u, k, sh = ctypes.windll.user32, ctypes.windll.kernel32, ctypes.windll.shell32
            u.DefWindowProcW.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM]; u.DefWindowProcW.restype = LRESULT
            u.CreateWindowExW.argtypes = [wt.DWORD, wt.LPCWSTR, wt.LPCWSTR, wt.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wt.HWND, wt.HMENU, wt.HINSTANCE, wt.LPVOID]
            u.CreateWindowExW.restype = wt.HWND
            u.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASS)]
            u.LoadImageW.argtypes = [wt.HINSTANCE, wt.LPCWSTR, wt.UINT, ctypes.c_int, ctypes.c_int, wt.UINT]; u.LoadImageW.restype = wt.HANDLE
            k.GetModuleHandleW.argtypes = [wt.LPCWSTR]; k.GetModuleHandleW.restype = wt.HMODULE
            sh.Shell_NotifyIconW.argtypes = [wt.DWORD, ctypes.POINTER(NID)]
            u.CreatePopupMenu.restype = wt.HMENU
            u.AppendMenuW.argtypes = [wt.HMENU, wt.UINT, ctypes.c_size_t, wt.LPCWSTR]
            u.TrackPopupMenu.argtypes = [wt.HMENU, wt.UINT, ctypes.c_int, ctypes.c_int, ctypes.c_int, wt.HWND, wt.LPVOID]
            u.SetForegroundWindow.argtypes = [wt.HWND]; u.DestroyMenu.argtypes = [wt.HMENU]; u.GetCursorPos.argtypes = [ctypes.POINTER(PT)]
            u.DestroyWindow.argtypes = [wt.HWND]; u.DestroyWindow.restype = wt.BOOL
            s.u, s.sh = u, sh
            s.proc = WNDPROC(s.wndproc)                                   # phải giữ tham chiếu
            hi = k.GetModuleHandleW(None)
            wc = WNDCLASS(); wc.lpfnWndProc = s.proc; wc.hInstance = hi; wc.lpszClassName = "PomoPetTray"
            u.RegisterClassW(ctypes.byref(wc))
            s.hwnd = u.CreateWindowExW(0, "PomoPetTray", "PomoPetTray", 0, 0, 0, 0, 0, wt.HWND(-3), None, hi, None)
            ico = os.path.join(tempfile.gettempdir(), "pomopet_tray.ico"); make_ico(ico)
            s.icon = u.LoadImageW(None, ico, 1, 0, 0, 0x10 | 0x40)       # IMAGE_ICON, LR_LOADFROMFILE | LR_DEFAULTSIZE
            s.ok = bool(s.hwnd) and bool(s.icon)
            if s.ok: s.notify(0, 1 | 2 | 4, "Pomodoro Pet")             # NIM_ADD
        except Exception:
            s.ok = False

    def nid(s, flags, tip=None, info=None, title=""):
        n = NID(); n.cbSize = ctypes.sizeof(NID); n.hWnd = s.hwnd; n.uID = 1; n.uFlags = flags; n.uCallbackMessage = s.CB; n.hIcon = s.icon
        if tip is not None: n.szTip = tip[:127]
        if info: n.szInfo = info[:255]; n.szInfoTitle = title[:63]; n.dwInfoFlags = 1
        return n
    def notify(s, op, flags, tip=None, info=None, title=""):
        try: s.sh.Shell_NotifyIconW(op, ctypes.byref(s.nid(flags, tip, info, title)))
        except Exception: pass
    def set_tip(s, text):
        if s.ok and text != s.tip: s.tip = text; s.notify(1, 1 | 2 | 4, text)      # NIM_MODIFY
    def balloon(s, title, msg):
        if s.ok: s.notify(1, 1 | 2 | 0x10, s.tip, msg, title)
    def remove(s):
        if s.ok: s.notify(2, 0); s.ok = False                                       # NIM_DELETE
        if s.hwnd and s.u.DestroyWindow(s.hwnd):
            s.hwnd = None; s.proc = None

    def wndproc(s, hwnd, msg, wp, lp):
        try:
            if msg == s.CB:
                ev = lp & 0xFFFF
                if ev in (0x201, 0x202, 0x203, 0x400, 0x401): s.events.put("restore")
                elif ev == 0x205: s.events.put("menu")                               # bấm phải: menu
                return 0
        except Exception: pass
        return s.u.DefWindowProcW(hwnd, msg, wp, lp)

    def menu(s):
        u, a = s.u, s.app
        m = u.CreatePopupMenu()
        u.AppendMenuW(m, 0, 1, "Mở Pomodoro Pet")
        toggle_label = "Đang nghỉ" if a.mode == "break" else "Tạm dừng" if a.running and a.mode == "focus" else "Bắt đầu / Tiếp tục"
        u.AppendMenuW(m, 0x1 if a.mode == "break" else 0, 2, toggle_label)
        u.AppendMenuW(m, 0x800, 0, None)
        u.AppendMenuW(m, 0, 3, "Thoát")
        pt = PT(); u.GetCursorPos(ctypes.byref(pt)); u.SetForegroundWindow(s.hwnd)
        cmd = u.TrackPopupMenu(m, 0x180, pt.x, pt.y, 0, s.hwnd, None)             # TPM_RETURNCMD | TPM_NONOTIFY
        u.DestroyMenu(m)
        if cmd == 1: a.root.after(0, a.restore)
        elif cmd == 2 and a.mode != "break": a.root.after(0, a.toggle)
        elif cmd == 3: a.root.after(0, a.quit)

# ====================== TỰ ĐO XAO NHÃNG ======================
def norm(t):
    """Chữ thường, bỏ dấu tiếng Việt để so khớp từ khóa."""
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn").replace("đ", "d")

try:
    _u, _k = ctypes.windll.user32, ctypes.windll.kernel32
    _u.GetForegroundWindow.restype = ctypes.c_void_p
    _u.GetWindowTextW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
    _u.GetWindowThreadProcessId.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
    _k.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]; _k.OpenProcess.restype = ctypes.c_void_p
    _k.QueryFullProcessImageNameW.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_ulong)]
    _k.CloseHandle.argtypes = [ctypes.c_void_p]; _k.GetTickCount.restype = ctypes.c_ulong
except Exception:
    pass

class LII(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def foreground():
    """(mã cửa sổ, tiêu đề, tên chương trình) của cửa sổ bạn đang dùng."""
    try:
        u, k = ctypes.windll.user32, ctypes.windll.kernel32
        h = u.GetForegroundWindow()
        if not h: return 0, "", ""
        buf = ctypes.create_unicode_buffer(512); u.GetWindowTextW(h, buf, 512)
        pid = ctypes.c_ulong(); u.GetWindowThreadProcessId(h, ctypes.byref(pid)); exe = ""
        hp = k.OpenProcess(0x1000, False, pid.value)             # PROCESS_QUERY_LIMITED_INFORMATION
        if hp:
            n, b = ctypes.c_ulong(520), ctypes.create_unicode_buffer(520)
            if k.QueryFullProcessImageNameW(hp, 0, b, ctypes.byref(n)): exe = os.path.basename(b.value)
            k.CloseHandle(hp)
        return h, buf.value, exe
    except Exception:
        return 0, "", ""

def idle_seconds():
    """Số giây kể từ lần gõ phím / di chuột gần nhất."""
    try:
        li = LII(); li.cbSize = ctypes.sizeof(LII)
        if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(li)): return 0
        return ((ctypes.windll.kernel32.GetTickCount() - li.dwTime) & 0xFFFFFFFF) / 1000.0
    except Exception:
        return 0

def score(d):
    if not isinstance(d, dict): return None
    t, good = d.get("total", 0), d.get("good", 0)
    numeric = lambda value: isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
    return round(100 * good / t) if numeric(t) and t > 0 and numeric(good) else None

def span(sec): return f"{sec} giây" if sec < 60 else f"{round(sec / 60)} phút"

def cause(d):
    """Nguyên nhân xao nhãng lớn nhất trong ngày, dạng câu ngắn."""
    c = [(v, f"xem {k} {span(v)}") for k, v in d.get("sites", {}).items()]
    c += [(d.get("idle", 0), f"rời máy {span(d.get('idle', 0))}"), (d.get("switch", 0), f"chuyển cửa sổ liên tục {span(d.get('switch', 0))}")]
    best = max(c, default=(0, ""))
    return best[1] if best[0] >= 20 else None


class Monitor:
    """Mỗi giây trong giờ tập trung, phân loại: tốt / vào trang xao nhãng / rời máy / chuyển cửa sổ liên tục.
       Chỉ lưu con số thống kê. Tiêu đề cửa sổ không bị lưu hay gửi đi đâu."""
    GRACE, IDLE, SW_N, SW_WIN = 10, 90, 8, 60      # ở trang xao nhãng >10s mới tính; không thao tác >90s; >=8 lần đổi cửa sổ/phút
    def __init__(s, app): s.app = app; s.compile(); s.reset()
    def compile(s):
        def pat(v): return [(k, re.compile(r"\b" + re.escape(k) + r"\b")) for k in (norm(x).strip() for x in v.split(",")) if k]
        s.bad, s.ok = pat(s.app.S["bad_kw"]), pat(s.app.S["ok_kw"])
    def match(s, title, exe):
        t = norm(title + " " + exe)
        if any(p.search(t) for _, p in s.ok): return None            # ngoại lệ (ví dụ "bài giảng")
        for k, p in s.bad:
            if p.search(t): return k
        return None
    def reset(s):
        s.total = s.good = s.idle = s.switch = s.episodes = s.run = s.pend = 0
        s.sites, s.run_site, s.last_hwnd, s.hw = {}, None, None, []
        s.idle_on = s.sw_on = False; s.state, s.label, s.alert = "good", "", None
    def pause(s):
        s.good += s.pend; s.pend = 0; s.run_site, s.run = None, 0
        s.last_hwnd, s.hw = None, []
        s.idle_on = s.sw_on = False; s.state, s.label, s.alert = "unknown", "", None
    def sample(s, now):
        h, title, exe = foreground()
        mine = "pomodoro pet" in norm(title)
        s.alert = None
        if title and not mine and h != s.last_hwnd: s.last_hwnd = h; s.hw.append(now)
        s.hw = [x for x in s.hw if now - x <= s.SW_WIN]
        if idle_seconds() >= s.IDLE:
            s.good += s.pend; s.pend = 0; s.run_site, s.run = None, 0
            s.total += 1; s.idle += 1; s.sw_on = False
            if not s.idle_on: s.idle_on = True; s.episodes += 1; s.alert = "bạn có đang rời máy không"
            s.state, s.label = "idle", ""
            return s.state
        if not h or not title or mine:
            s.good += s.pend; s.pend = 0; s.run_site, s.run = None, 0
            s.idle_on = s.sw_on = False
            s.state, s.label = "unknown", ""
            return s.state
        kw = s.match(title, exe)
        s.total += 1
        if kw:
            if kw != s.run_site: s.good += s.pend; s.pend = 0; s.run_site, s.run = kw, 0
            s.run += 1; s.idle_on = s.sw_on = False; state = "site"
            if s.run < s.GRACE: s.pend = s.run                          # còn trong thời gian chờ, chưa tính
            else:
                s.sites[kw] = s.sites.get(kw, 0) + (s.GRACE if s.run == s.GRACE else 1); s.pend = 0
                if s.run == s.GRACE: s.episodes += 1; s.alert = f"bạn đang xem {kw}"
        else:
            s.good += s.pend; s.pend = 0; s.run_site, s.run = None, 0
            if len(s.hw) >= s.SW_N:
                state = "switch"; s.switch += 1; s.idle_on = False
                if not s.sw_on: s.sw_on = True; s.episodes += 1; s.alert = "bạn đang chuyển cửa sổ liên tục"
            else:
                state = "good"; s.good += 1; s.idle_on = s.sw_on = False
        s.state, s.label = state, kw or ""
        return state
    def result(s):
        s.good += s.pend; s.pend = 0
        return {"total": s.total, "good": s.good, "idle": s.idle, "switch": s.switch, "episodes": s.episodes,
                "sites": dict(s.sites), "score": round(100 * s.good / s.total) if s.total else None}


# ====================== ỨNG DỤNG CHÍNH ======================
class App:
    def __init__(s, root):
        s.root = root
        root.title("Pomodoro Pet"); root.configure(bg=BG)
        root.report_callback_exception = lambda exc, val, tb: log("".join(traceback.format_exception(exc, val, tb)))
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        W, H = min(z(480), int(sw * .9)), min(z(780), int(sh * .88))
        root.geometry(f"{W}x{H}+{(sw - W) // 2}+{max(0, (sh - H) // 3)}"); root.minsize(z(360), z(480))
        s.db = {"s": {"focus": 25, "brk": 5, "pet": "Mèo", "music": "lofi", "vol": "Vừa", "strict": False, "wav": "", "auto": True, "bad_kw": "facebook, youtube, tiktok, zalo, messenger, instagram, netflix, shopee, lazada, threads, twitter, reddit, steam, league of legends, valorant, genshin, minecraft, roblox", "ok_kw": "bai giang, hoc, khoa hoc, tutorial, lecture, course, excel, word, powerpoint"}, "days": {}}
        try:
            with open(DATA, encoding="utf-8") as f:
                d = json.load(f)
                if isinstance(d, dict):
                    saved_settings, saved_days = d.get("s", {}), d.get("days", {})
                    if isinstance(saved_settings, dict): s.db["s"].update(saved_settings)
                    if isinstance(saved_days, dict): s.db["days"] = saved_days
        except Exception: pass
        S = s.S = s.db["s"]
        for key, default in tuple(S.items()):
            if type(S[key]) is not type(default): S[key] = default
        S["focus"] = max(1, min(1440, S["focus"]))
        S["brk"] = max(1, min(1440, S["brk"]))
        for key in ("focus", "brk"):
            seconds_key = key + "_seconds"
            seconds = S.get(seconds_key, S[key] * 60)
            if not isinstance(seconds, int) or isinstance(seconds, bool) or not 1 <= seconds <= 86399:
                seconds = S[key] * 60
            S[seconds_key] = seconds
        if S["pet"] not in PETS: S["pet"] = "Mèo"
        if S["music"] not in {key for key, _ in MUS}: S["music"] = "off"
        if S["vol"] not in VOLS: S["vol"] = "Vừa"
        s.mode, s.running, s.deadline, s.remaining, s.total, s.token, s.ov, s.t0, s.refreshers = "idle", False, 0, S["focus_seconds"], 0, 0, None, time.time(), []
        s.session_started = None
        s.break_continues = False
        s.dirty, s.stats_txt, s.hidden, s.tab = False, "", False, "main"
        s.mon = Monitor(s); s.last_sample = s.last_nudge = 0.0

        top = tk.Frame(root, bg=BG); top.pack(fill="x", padx=z(14), pady=(z(12), z(4)))
        s.tabs = {}
        for k, t in (("main", "Tập trung"), ("stats", "Thống kê"), ("set", "Cài đặt")):
            b = Btn(top, t, lambda k=k: s.show(k), bg=CARD, sel=ACC, size=10, padx=20, pady=7); b.pack(side="left", padx=(0, z(8))); s.tabs[k] = b
        s.pages = {"main": tk.Frame(root, bg=BG), "stats": Scroll(root, BG), "set": Scroll(root, BG)}

        # --- trang Tập trung ---
        m = s.pages["main"]
        s.msg = tk.Label(m, bg=BG, fg=GOLD, font=F(11, True), justify="center", height=3, wraplength=z(380)); s.msg.pack(side="bottom", fill="x", pady=(0, z(10)))
        s.stats = tk.Label(m, bg=BG, fg=MUTE, font=F(10)); s.stats.pack(side="bottom", pady=(z(6), z(4)))
        bar = tk.Frame(m, bg=BG); bar.pack(side="bottom", pady=z(8))
        s.btn = Btn(bar, "Bắt đầu", s.toggle, bg=ACC, size=14, padx=36, pady=12, texts=["Bắt đầu", "Tạm dừng", "Tiếp tục"]); s.btn.pack(side="left", padx=z(6))
        Btn(bar, "Đặt lại", s.reset, size=11, pady=11).pack(side="left", padx=z(6))
        s.hero = tk.Canvas(m, bg=BG, highlightthickness=0); s.hero.pack(side="top", fill="both", expand=True)
        m.bind("<Configure>", lambda e: s.msg.config(wraplength=max(z(200), e.width - z(40))))

        # --- trang Thống kê ---
        SI = s.pages["stats"].inner
        export_bar = tk.Frame(SI, bg=BG); export_bar.pack(fill="x", padx=z(14), pady=(z(10), z(4)))
        Btn(export_bar, "Xuất CSV cho Excel", s.export_csv, bg=ACC, size=10, padx=16, pady=8).pack(side="left")
        s.stats_summary = tk.Label(SI, text="", bg=BG, fg=MUTE, font=F(9), justify="left", wraplength=z(420))
        s.stats_summary.pack(fill="x", padx=z(16), pady=(z(2), z(6)))
        s.focus_chart = tk.Canvas(SI, height=z(180), bg=CARD, highlightthickness=0)
        s.focus_chart.pack(fill="x", padx=z(14), pady=z(5))
        s.distract_chart = tk.Canvas(SI, height=z(180), bg=CARD, highlightthickness=0)
        s.distract_chart.pack(fill="x", padx=z(14), pady=z(5))
        s.session_chart = tk.Canvas(SI, height=z(180), bg=CARD, highlightthickness=0)
        s.session_chart.pack(fill="x", padx=z(14), pady=(z(5), z(12)))
        for chart in (s.focus_chart, s.distract_chart, s.session_chart):
            chart.bind("<Configure>", lambda e: s.draw_stats())

        # --- trang Cài đặt (nhạc nằm ở đây) ---
        I = s.pages["set"].inner
        def card(title):
            f = tk.Frame(I, bg=CARD); f.pack(fill="x", padx=z(14), pady=z(6))
            tk.Label(f, text=title, bg=CARD, fg=MUTE, font=F(9)).pack(anchor="w", padx=z(14), pady=(z(10), z(4)))
            return f
        c1 = card("Thời gian")
        s.duration_input(c1, "Tập trung", "focus"); s.duration_input(c1, "Nghỉ ngắn", "brk"); tk.Frame(c1, bg=CARD, height=z(8)).pack()
        s.chips(card("Bạn đồng hành"), [(p, p) for p in PETS], "pet")
        s.chips(card("Nhạc khi nghỉ (bấm để nghe thử)"), MUS, "music", s.pick_music)
        s.chips(card("Âm lượng"), [(v, v) for v in VOLS], "vol", s.pick_music)
        s.chips(card("Chế độ nghiêm: không cho thoát giờ nghỉ"), [(False, "Tắt"), (True, "Bật")], "strict")
        s.chips(card("Tự đo xao nhãng (đọc tên cửa sổ, thời gian không thao tác, tần suất chuyển cửa sổ)"), [(True, "Bật"), (False, "Tắt")], "auto")
        def kwbox(title, key):
            f = card(title)
            t = tk.Text(f, height=3, wrap="word", bg=CHIP, fg="#fff", insertbackground="#fff", relief="flat", font=F(10), padx=8, pady=6)
            t.insert("1.0", s.S[key]); t.pack(fill="x", padx=z(14), pady=(0, z(10)))
            def sv(e=None): s.S[key] = t.get("1.0", "end").strip(); s.dirty = True; s.mon.compile()
            t.bind("<KeyRelease>", sv); t.bind("<FocusOut>", sv)
        kwbox("Trang / ứng dụng bị coi là xao nhãng (cách nhau bằng dấu phẩy, không cần gõ dấu)", "bad_kw")
        kwbox("Ngoại lệ: tiêu đề chứa từ này thì KHÔNG tính là xao nhãng", "ok_kw")
        c5 = card("Thử đo")
        Btn(c5, "Thử đo cửa sổ sau 5 giây", s.probe, size=10, padx=18, pady=8).pack(anchor="w", padx=z(14), pady=(0, z(6)))
        s.probe_lbl = tk.Label(c5, text="Bấm nút, rồi chuyển sang cửa sổ bạn muốn thử (ví dụ trang YouTube).", bg=CARD, fg=MUTE, font=F(9), wraplength=z(380), justify="left")
        s.probe_lbl.pack(anchor="w", padx=z(14), pady=(0, z(10)))
        c6 = card("Thử ngay"); Btn(c6, "Xem thử giờ nghỉ (12 giây)", s.preview, size=10, padx=18, pady=8).pack(anchor="w", padx=z(14), pady=(0, z(12)))
        root.bind_all("<MouseWheel>", lambda e: s.tab in ("set", "stats") and s.pages[s.tab].wheel(e))

        root.protocol("WM_DELETE_WINDOW", s.quit)
        s.tray = Tray(s); root.bind("<Unmap>", s.on_unmap)             # thu nhỏ -> vào khay hệ thống
        s.show("main"); s.warm(); s.tick(); s.frame()

    # --- dựng giao diện ---
    def show(s, k):
        s.tab = k
        for pg in s.pages.values(): pg.pack_forget()
        s.pages[k].pack(fill="both", expand=True)
        for kk, b in s.tabs.items(): b.set(on=(kk == k))
        if k == "stats": s.draw_stats()
    def duration_seconds(s, key):
        return s.S.get(key + "_seconds", s.S[key] * 60)
    def update_duration(s, key, seconds):
        s.S[key + "_seconds"] = seconds
        s.S[key] = max(1, int(math.ceil(seconds / 60)))
        s.dirty = True
        if s.mode == "idle" and key == "focus": s.remaining = seconds
    def duration_input(s, p, label, key):
        row = tk.Frame(p, bg=CARD); row.pack(fill="x", padx=z(14), pady=z(7))
        header = tk.Frame(row, bg=CARD); header.pack(fill="x")
        tk.Label(header, text=label, bg=CARD, fg="#fff", font=F(11, True)).pack(side="left")
        seconds = s.duration_seconds(key)
        hours, remainder = divmod(seconds, 3600); minutes, seconds = divmod(remainder, 60)
        fields, entries = [], []
        fields_row = tk.Frame(row, bg=CARD); fields_row.pack(fill="x", pady=(z(5), 0))
        for value, unit_key, unit, limit in ((hours, "hours", "Giờ", 23), (minutes, "minutes", "Phút", 59), (seconds, "seconds", "Giây", 59)):
            group = tk.Frame(fields_row, bg=CARD); group.pack(side="left", fill="x", expand=True, padx=(0, z(6)))
            tk.Label(group, text=unit, bg=CARD, fg=MUTE, font=F(9)).pack(anchor="w", pady=(0, z(2)))
            var = tk.StringVar(value=f"{value:02d}")
            entry = tk.Entry(group, textvariable=var, width=5, justify="center", bg=CHIP, fg="#fff", insertbackground="#fff", relief="flat", font=F(12, True))
            entry.pack(fill="x", ipady=z(5))
            entries.append(entry)
            fields.append((var, unit_key, limit))
        def refresh():
            current = s.duration_seconds(key)
            h, rest = divmod(current, 3600); m, sec = divmod(rest, 60)
            parts = {"hours": h, "minutes": m, "seconds": sec}
            for var, unit_key, _ in fields: var.set(f"{parts[unit_key]:02d}")
        def commit(event=None):
            try:
                values = {unit_key: int(var.get()) for var, unit_key, _ in fields}
                if any(values[unit_key] < 0 or values[unit_key] > limit for _, unit_key, limit in fields): raise ValueError
                total = values["hours"] * 3600 + values["minutes"] * 60 + values["seconds"]
                if total < 1: raise ValueError
            except ValueError:
                refresh(); return
            s.update_duration(key, total)
            refresh()
        for entry in entries:
            entry.bind("<Return>", commit); entry.bind("<FocusOut>", commit)
            entry.bind("<FocusIn>", lambda event: event.widget.selection_range(0, tk.END))
        def adjust(delta):
            current = max(1, min(86399, s.duration_seconds(key) + delta * 60))
            s.update_duration(key, current); refresh()
        Btn(header, "+", lambda: adjust(1), size=10, padx=9, pady=3, repeat=True, bgp=CARD).pack(side="right", padx=(z(4), 0))
        Btn(header, "−", lambda: adjust(-1), size=10, padx=9, pady=3, repeat=True, bgp=CARD).pack(side="right", padx=(z(4), 0))
    def chips(s, p, items, key, cmd=None):
        fl = Flow(p, bg=CARD, height=1); fl.pack(fill="x", padx=z(11), pady=(0, z(10))); btns = {}
        def refresh():
            for v, b in btns.items(): b.set(on=(s.S[key] == v))
        def pick(v):
            changed = s.S[key] != v
            s.S[key] = v
            if key == "auto" and changed and s.mode == "focus":
                s.mon.pause(); s.last_sample = time.monotonic()
            s.save(); cmd and cmd(); [r() for r in s.refreshers]
        for v, t in items:
            b = Btn(fl, t, lambda v=v: pick(v), bg=CHIP, sel=ACC, size=10, padx=14, pady=7, bgp=CARD); fl.add(b); btns[v] = b
        s.refreshers.append(refresh); refresh()

    # --- dữ liệu ---
    def save(s):
        s.dirty = False
        try:
            with open(DATA, "w", encoding="utf-8") as f: json.dump(s.db, f, ensure_ascii=False)
        except Exception: pass
    def day(s, off=0):
        k = (dt.date.today() - dt.timedelta(days=off)).isoformat()
        d = s.db["days"].get(k)
        if not isinstance(d, dict): d = s.db["days"][k] = {"focus": 0, "distract": 0}
        for key in ("focus", "distract", "total", "good", "idle", "switch"):
            value = d.get(key, 0)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0: d[key] = 0
        sites = d.get("sites", {})
        d["sites"] = {key: value for key, value in sites.items() if isinstance(key, str) and isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0} if isinstance(sites, dict) else {}
        return d
    def record_session(s, r):
        d = s.day(); minutes = max(1, int(s.total // 60))
        d["focus"] += minutes
        tracked = bool(s.S["auto"] and r["total"])
        if tracked:
            for key, value in (("total", r["total"]), ("good", r["good"]), ("distract", r["episodes"]), ("idle", r["idle"]), ("switch", r["switch"])):
                d[key] = d.get(key, 0) + value
            sites = d.setdefault("sites", {})
            for key, value in r["sites"].items(): sites[key] = sites.get(key, 0) + value
        sessions = d.get("sessions")
        if not isinstance(sessions, list): sessions = d["sessions"] = []
        sessions.append({
            "started": s.session_started or dt.datetime.now().isoformat(timespec="seconds"),
            "minutes": minutes,
            "score": r["score"] if tracked else None,
            "tracked_seconds": r["total"] if tracked else 0,
            "good_seconds": r["good"] if tracked else 0,
            "distract_count": r["episodes"] if tracked else 0,
            "idle_seconds": r["idle"] if tracked else 0,
            "switch_seconds": r["switch"] if tracked else 0,
            "sites": dict(r["sites"]) if tracked else {},
        })
        s.session_started = None
    def export_rows(s):
        header = ["Loại bản ghi", "Ngày", "Phiên", "Bắt đầu", "Phút tập trung", "Điểm tập trung", "Giây đã đo", "Giây tập trung tốt", "Số đợt xao nhãng", "Giây rời máy", "Giây chuyển cửa sổ", "Thời gian theo từ khóa (JSON)"]
        rows = [header]
        safe = lambda value: "'" + value if isinstance(value, str) and value.startswith(("=", "+", "-", "@", "\t", "\r")) else value
        for date, day in sorted(s.db.get("days", {}).items(), key=lambda item: str(item[0])):
            if not isinstance(date, str) or not isinstance(day, dict): continue
            rows.append(["Ngày", date, "", "", day.get("focus", 0), score(day), day.get("total", 0), day.get("good", 0), day.get("distract", 0), day.get("idle", 0), day.get("switch", 0), json.dumps(day.get("sites", {}), ensure_ascii=False, sort_keys=True)])
            sessions = day.get("sessions", [])
            if not isinstance(sessions, list): continue
            for index, session in enumerate(sessions, 1):
                if not isinstance(session, dict): continue
                rows.append(["Phiên", date, index, session.get("started", ""), session.get("minutes", 0), session.get("score"), session.get("tracked_seconds", 0), session.get("good_seconds", 0), session.get("distract_count", 0), session.get("idle_seconds", 0), session.get("switch_seconds", 0), json.dumps(session.get("sites", {}), ensure_ascii=False, sort_keys=True)])
        return [[safe(value) for value in row] for row in rows]
    def export_csv(s):
        path = filedialog.asksaveasfilename(parent=s.root, title="Xuất thống kê cho Excel", defaultextension=".csv", filetypes=[("CSV mở bằng Excel", "*.csv")])
        if not path: return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                csv.writer(f).writerows(s.export_rows())
            s.stats_summary.config(text=f"Đã xuất dữ liệu: {os.path.basename(path)}")
        except Exception:
            log(); s.stats_summary.config(text="Không xuất được file. Hãy chọn vị trí khác rồi thử lại.")
    def draw_stats(s):
        days = s.db.get("days", {})
        if not isinstance(days, dict): days = {}
        today = dt.date.today()
        numeric = lambda value: isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0
        metric = lambda data, key: data.get(key, 0) if numeric(data.get(key, 0)) else 0
        daily = []
        for offset in range(13, -1, -1):
            date = today - dt.timedelta(days=offset); data = days.get(date.isoformat(), {})
            if not isinstance(data, dict): data = {}
            daily.append((date.strftime("%d/%m"), data))
        sessions = []
        for date, data in sorted(days.items(), key=lambda item: str(item[0])):
            if isinstance(date, str) and isinstance(data, dict) and isinstance(data.get("sessions"), list):
                sessions.extend((date, session) for session in data["sessions"] if isinstance(session, dict))
        all_sessions = sessions
        sessions = all_sessions[-10:]
        total_sessions = sum(len(data.get("sessions", [])) for data in days.values() if isinstance(data, dict) and isinstance(data.get("sessions"), list))
        total_minutes = sum(metric(data, "focus") for data in days.values() if isinstance(data, dict))
        scored = [session["score"] for _, session in all_sessions if numeric(session.get("score")) and session.get("score") <= 100]
        if total_sessions:
            average = round(sum(scored) / len(scored)) if scored else None
            average_text = f" · TB tập trung {average}/100 · TB xao nhãng {100 - average}/100" if average is not None else " · Chưa có điểm để tính trung bình"
            s.stats_summary.config(text=f"{total_sessions} phiên đã hoàn thành · {total_minutes} phút tập trung{average_text} · Biểu đồ ngày: 14 ngày gần nhất")
        else:
            s.stats_summary.config(text="Chưa có phiên hoàn thành mới. Chi tiết từng phiên được lưu từ khi bật bản này; tổng ngày cũ vẫn được giữ.")

        def bars(canvas, title, rows, color, limit=None):
            canvas.delete("all")
            width, height = max(canvas.winfo_width(), z(280)), max(canvas.winfo_height(), z(160))
            left, right, top, bottom = z(38), width - z(12), z(24), height - z(28)
            values = [value for _, value in rows if numeric(value)]
            maximum = limit or max(values, default=0) or 1
            canvas.create_text(left, z(12), text=title, fill="#ffffff", anchor="w", font=F(9, True))
            for fraction in (0, .5, 1):
                y = bottom - (bottom - top) * fraction
                canvas.create_line(left, y, right, y, fill=CHIP)
                canvas.create_text(left - z(5), y, text=f"{maximum * fraction:g}", fill=MUTE, anchor="e", font=F(8))
            if not rows:
                canvas.create_text(width / 2, (top + bottom) / 2, text="Chưa có dữ liệu", fill=MUTE, font=F(9))
                return
            slot = (right - left) / len(rows)
            bar_width = max(z(4), min(z(22), slot * .58))
            for index, (label, value) in enumerate(rows):
                center = left + slot * (index + .5)
                if numeric(value):
                    number = max(0, min(maximum, value))
                    y = bottom - (bottom - top) * number / maximum
                    canvas.create_rectangle(center - bar_width / 2, y, center + bar_width / 2, bottom, fill=color, outline="")
                    if len(rows) <= 10:
                        canvas.create_text(center, max(top + z(7), y - z(8)), text=f"{value:g}", fill="#ffffff", font=F(8))
                else:
                    canvas.create_text(center, bottom - z(8), text="—", fill=MUTE, font=F(8))
                if len(rows) <= 10 or index % 2 == 0:
                    canvas.create_text(center, bottom + z(13), text=label, fill=MUTE, font=F(8))

        bars(s.focus_chart, "Phút tập trung mỗi ngày", [(label, metric(data, "focus")) for label, data in daily], "#6ec6ff")
        bars(s.distract_chart, "Số đợt xao nhãng mỗi ngày", [(label, metric(data, "distract")) for label, data in daily], "#ffb02e")
        score_rows = [(f"{index + 1}", session.get("score") if numeric(session.get("score")) and session.get("score") <= 100 else None) for index, (_, session) in enumerate(sessions)]
        bars(s.session_chart, "Điểm tập trung mỗi phiên gần nhất (thang 100)", score_rows, "#76d7a8", 100)
    def feedback(s, r):
        sess = r["score"]
        if not s.S["auto"] or sess is None: return "Xong một phiên! Nghỉ ngơi thôi."
        y = s.db["days"].get((dt.date.today() - dt.timedelta(days=1)).isoformat())
        t, head = s.day(), f"Phiên này: {sess}/100."
        ts, ys = score(t), score(y)
        if ts is None or ys is None: return head + " Ngày mai mình sẽ so sánh với hôm nay nhé."
        diff, cs = ts - ys, cause(t)
        if diff >= 5: return f"{head} Hôm nay tập trung hơn hôm qua {diff} điểm ({ts} so với {ys}). Giữ vững nhé!"
        if diff > -5: return f"{head} Ngang ngửa hôm qua ({ts} so với {ys}). Cố thêm chút nữa nào!"
        return f"{head} Hôm nay thấp hơn hôm qua {-diff} điểm ({ts} so với {ys})." + (f" Nguyên nhân chính: {cs}. Thử đóng nó lại nhé!" if cs else " Hãy chú tâm hơn nhé!")
    def nudge(s, text):
        now = time.monotonic()
        if now - s.last_nudge < 90: return
        s.last_nudge = now; s.tray.balloon("Quay lại làm việc nào!", text[:1].upper() + text[1:])
    def probe(s):
        s.probe_lbl.config(text="Đang đo sau 5 giây... hãy chuyển sang cửa sổ cần thử.")
        s.root.after(5000, s.do_probe)
    def do_probe(s):
        h, title, exe = foreground()
        if "pomodoro pet" in norm(title) or not title: s.probe_lbl.config(text="Chưa thấy cửa sổ nào khác. Hãy thử lại và chuyển sang cửa sổ khác trong 5 giây."); return
        kw = s.mon.match(title, exe)
        s.probe_lbl.config(text=f"Cửa sổ: «{title[:50]}»  →  " + (f"XAO NHÃNG (khớp \"{kw}\")" if kw else "bình thường"))

    # --- nhạc ---
    def warm(s):
        """Tạo sẵn file nhạc ở nền ngay khi mở app, để lúc nghỉ không phải chờ."""
        k, vol = s.S["music"], VOLS.get(s.S["vol"], .6)
        if winsound and k in ("lofi", "rain", "sea"):
            def run():
                try: ensure_wav(k, vol)
                except Exception: log()
            threading.Thread(target=run, daemon=True).start()
    def music(s, kind):
        s.token += 1; tok = s.token
        if not winsound: return
        try: winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception: pass
        if kind == "off": return
        vol, wav = VOLS.get(s.S["vol"], .6), s.S["wav"]
        def run():
            try:
                path = wav if kind == "file" else ensure_wav(kind, vol)
                if path and os.path.exists(path) and tok == s.token:
                    winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
            except Exception: log()
        threading.Thread(target=run, daemon=True).start()
    def pick_music(s):
        S = s.S
        if S["music"] == "file":
            p = filedialog.askopenfilename(filetypes=[("WAV", "*.wav")])
            if p: S["wav"] = p
            else: S["music"] = "off"
            [r() for r in s.refreshers]; s.save()
        s.music(S["music"]); tok = s.token
        s.root.after(6000, lambda: tok == s.token and s.mode != "break" and s.music("off"))
    def chime(s):
        if winsound:
            def run():
                try:
                    for f in (660, 880, 1320): winsound.Beep(f, 150)
                except Exception: pass
            threading.Thread(target=run, daemon=True).start()

    # --- đồng hồ ---
    def fmt(s, sec):
        if sec >= 3600: return f"{sec // 3600:02d}:{(sec % 3600) // 60:02d}:{sec % 60:02d}"
        return f"{sec // 60:02d}:{sec % 60:02d}"
    def status_text(s):
        if s.mode == "focus" and s.running and s.S["auto"]:
            m = s.mon
            if m.state == "site": return f"Đang xao nhãng: {m.label}"
            if m.state == "idle": return "Bạn đang rời máy?"
            if m.state == "switch": return "Chuyển cửa sổ liên tục"
            if m.state == "unknown": return "Đang đo hoạt động..."
        return {"idle": "Sẵn sàng", "break": "Đang nghỉ"}.get(s.mode, "Đang tập trung" if s.running else "Đã tạm dừng")
    def toggle(s):
        if s.mode == "idle":
            s.start_focus()
        elif s.mode == "focus" and s.running:
            s.running = False; s.mon.pause()
        elif s.mode == "focus":
            s.deadline = time.monotonic() + s.remaining; s.running = True; s.last_sample = time.monotonic()
    def reset(s):
        s.end_break(); s.mode, s.running, s.total = "idle", False, 0; s.remaining = s.duration_seconds("focus"); s.mon.reset()
    def start_focus(s):
        s.mode = "focus"; s.total = s.remaining = s.duration_seconds("focus")
        s.deadline = time.monotonic() + s.remaining; s.running = True; s.msg.config(text="")
        s.session_started = dt.datetime.now().isoformat(timespec="seconds")
        s.mon.reset(); s.last_sample = time.monotonic()
    def tick(s):
        try:
            while True:
                try: event = s.tray.events.get_nowait()
                except queue.Empty: break
                if event == "restore": s.restore()
                elif event == "menu": s.tray.menu()
            if s.running:
                s.remaining = max(0, int(math.ceil(s.deadline - time.monotonic())))
                if s.mode == "focus" and s.S["auto"] and s.remaining > 0 and time.monotonic() - s.last_sample >= 1:
                    s.last_sample = time.monotonic(); s.mon.sample(s.last_sample)
                    if s.mon.alert: s.nudge(s.mon.alert)
                if s.remaining <= 0: s.finish()
            s.tray.set_tip(f"Pomodoro Pet · {s.fmt(s.remaining)} · {s.status_text()}" if s.mode != "idle" else "Pomodoro Pet · Sẵn sàng")
            s.root.title((s.fmt(s.remaining) + " · " if s.mode != "idle" else "") + "Pomodoro Pet")
            if s.dirty: s.save()
        except Exception: log()
        finally: s.root.after(200, s.tick)
    def finish(s):
        s.running = False; s.chime()
        if s.mode == "focus":
            r = s.mon.result(); s.record_session(r)
            s.save(); s.msg.config(text=s.feedback(r)); s.start_break(s.duration_seconds("brk"))
        else: s.end_break(True)
    def start_break(s, sec, continue_session=True):
        s.break_continues = continue_session
        s.mode = "break"; s.total = s.remaining = sec; s.deadline = time.monotonic() + sec; s.running = True
        try: s.ov = Overlay(s, s.S["pet"], bool(s.S["strict"]))
        except Exception: log(); s.ov = None
        s.music(s.S["music"])
    def end_break(s, bring_back=False):
        if s.ov: s.ov.close(); s.ov = None
        continue_session = s.break_continues
        s.break_continues = False
        if s.mode == "break":
            s.music("off"); s.mode, s.running, s.total = "idle", False, 0; s.remaining = s.duration_seconds("focus")
            if s.hidden:
                if bring_back: s.tray.balloon("Hết giờ nghỉ", s.msg.cget("text") or "Sẵn sàng cho phiên mới!")
            else: s.restore()
        if bring_back:
            s.show("main")
            if continue_session: s.start_focus()
    def preview(s):
        if s.mode == "idle": s.start_break(12, False)
    def quit(s):
        s.save(); s.music("off"); s.tray.remove()
        if s.ov: s.ov.close()
        s.root.destroy()
    def on_unmap(s, e):
        if e.widget is s.root and s.tray.ok and s.root.state() == "iconic": s.root.after(50, s.to_tray)
    def to_tray(s):
        if s.root.state() == "iconic": s.root.withdraw(); s.hidden = True      # ẩn khỏi taskbar, chỉ còn icon ở khay
    def restore(s):
        r = s.root; s.hidden = False
        r.deiconify(); r.state("normal"); r.lift(); r.attributes("-topmost", True); r.after(400, lambda: r.attributes("-topmost", False))
        try: r.focus_force()
        except Exception: pass

    # --- vẽ màn hình chính (tự co giãn; tạm nghỉ vẽ khi bị ẩn hoặc đang có lớp phủ nghỉ) ---
    def frame(s):
        delay = 50
        try:
            if s.hidden or s.mode == "break" or s.root.state() == "iconic":
                delay = 250
            else:
                c, t = s.hero, time.time() - s.t0
                c.delete("all")
                cw, ch = max(c.winfo_width(), 100), max(c.winfo_height(), 100)
                ps = max(60, min(cw * .5, ch * .36)); rd = max(90, min(cw * .8, ch - ps - z(20)))
                cx, py = cw / 2, z(4); ty = py + ps + z(8); lw = max(8, rd * .065)
                c.create_oval(cx - ps * .3, py + ps * .93, cx + ps * .3, py + ps * .99, fill="#0d0a1f", outline="")
                draw_pet(c, s.S["pet"], cx - ps / 2, py, ps, t)
                box = (cx - rd / 2 + lw / 2, ty + lw / 2, cx + rd / 2 - lw / 2, ty + rd - lw / 2)
                c.create_oval(*box, outline=CHIP, width=lw)
                frac = s.remaining / s.total if s.total else 1
                c.create_arc(*box, start=90, extent=-min(359.9, 360 * frac), style="arc", outline=ACC, width=lw)
                mid = ty + rd / 2
                c.create_text(cx, mid - rd * .04, text=s.fmt(s.remaining), fill="#ffffff", font=F(max(12, int(rd * .19 * .75 / Z)), True))
                c.create_text(cx, mid + rd * .17, text=s.status_text(), fill=(ACC if s.running and s.mode == "focus" and s.mon.state != "good" and s.S["auto"] else MUTE), font=F(max(9, int(rd * .065 * .75 / Z))))
                d = s.day(); sc = score(d); txt = f"Hôm nay: {d['focus']} phút tập trung" + (f" · điểm {sc}/100 · {d['distract']} lần xao nhãng" if sc is not None else "")
                if txt != s.stats_txt: s.stats_txt = txt; s.stats.config(text=txt)
                s.btn.set(text="Tạm dừng" if s.running and s.mode == "focus" else "Tiếp tục" if s.mode == "focus" else "Bắt đầu")
        except Exception: log()
        finally: s.root.after(delay, s.frame)


if __name__ == "__main__":
    root = tk.Tk()
    Z = max(1.0, root.winfo_fpixels("1i") / 96)
    App(root)
    root.mainloop()
