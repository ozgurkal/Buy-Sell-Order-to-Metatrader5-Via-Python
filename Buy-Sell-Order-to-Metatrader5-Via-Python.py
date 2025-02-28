import tkinter as tk
from tkinter import messagebox, ttk
import MetaTrader5 as mt5
import threading
import time


def sembolleri_yukle():
    try:
        with open("semboller.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        messagebox.showerror("Hata", "semboller.txt dosyası bulunamadı!")
        return []


def fiyat_guncelle():
    while True:
        secilen = sembol_combobox.get()
        if secilen and mt5.initialize():
            tick = mt5.symbol_info_tick(secilen)
            if tick:
                alis_fiyati_label.config(text=f"Alış: {tick.ask}")
                satis_fiyati_label.config(text=f"Satış: {tick.bid}")
            else:
                alis_fiyati_label.config(text="Alış: --")
                satis_fiyati_label.config(text="Satış: --")
            mt5.shutdown()
        time.sleep(1)


def Hisse_Al():
    hisse = sembol_combobox.get()
    try:
        fiyat = float(fiyat_entry.get())
        hacim = float(hacim_entry.get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")
        return

    if not mt5.initialize():
        messagebox.showerror("Hata", f"MT5 bağlantı hatası! {mt5.last_error()}")
        return

    order_request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": hisse,
        "volume": hacim,
        "type": mt5.ORDER_TYPE_BUY_LIMIT,
        "price": fiyat,
        "deviation": 10,
        "magic": 1000,
        "comment": "Python Buy Limit Order Test",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(order_request)

    if order_result is None:
        messagebox.showerror("Hata", f"Emir gönderilemedi! Hata: {mt5.last_error()}")
    elif order_result.retcode != mt5.TRADE_RETCODE_DONE:
        messagebox.showerror("Hata", f"Emir gönderilemedi! Kod: {order_result.retcode}\nDetaylar: {order_result}")
    else:
        messagebox.showinfo("Başarı", f"Buy Limit emri başarıyla gönderildi! Ticket: {order_result.order}")

    mt5.shutdown()


def Hisse_Sat():
    hisse = sembol_combobox.get()
    try:
        fiyat = float(fiyat_entry.get())
        hacim = float(hacim_entry.get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")
        return

    if not mt5.initialize():
        messagebox.showerror("Hata", f"MT5 bağlantı hatası! {mt5.last_error()}")
        return

    order_request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": hisse,
        "volume": hacim,
        "type": mt5.ORDER_TYPE_SELL_LIMIT,
        "price": fiyat,
        "deviation": 10,
        "magic": 1000,
        "comment": "Python Sell Limit Order Test",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(order_request)

    if order_result is None:
        messagebox.showerror("Hata", f"Emir gönderilemedi! Hata: {mt5.last_error()}")
    elif order_result.retcode != mt5.TRADE_RETCODE_DONE:
        messagebox.showerror("Hata", f"Emir gönderilemedi! Kod: {order_result.retcode}\nDetaylar: {order_result}")
    else:
        messagebox.showinfo("Başarı", f"Sell Limit emri başarıyla gönderildi! Ticket: {order_result.order}")

    mt5.shutdown()


# Tkinter Arayüzü
tk_root = tk.Tk()
tk_root.title("MT5 Alım Satım Test Uygulaması")
def Ekrani_Ortala(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")


Ekrani_Ortala(tk_root, 300, 150)  # 400x300 boyutunda ortalanmış pencere




tk.Label(tk_root, text="Hisse Sembolü:").grid(row=0, column=0)
sembol_combobox = ttk.Combobox(tk_root, state="readonly")
sembol_combobox.grid(row=0, column=1)
sembol_combobox['values'] = sembolleri_yukle()

tk.Label(tk_root, text="Alış Fiyatı:").grid(row=1, column=0)
fiyat_entry = tk.Entry(tk_root)
fiyat_entry.grid(row=1, column=1)

tk.Label(tk_root, text="Lot Miktarı:").grid(row=2, column=0)
hacim_entry = tk.Entry(tk_root)
hacim_entry.grid(row=2, column=1)

alis_fiyati_label = tk.Label(tk_root, text="Alış: --")
alis_fiyati_label.grid(row=3, column=0, columnspan=2)

satis_fiyati_label = tk.Label(tk_root, text="Satış: --")
satis_fiyati_label.grid(row=4, column=0, columnspan=2)

alis_buton = tk.Button(tk_root, text="AL", command=Hisse_Al, bg="blue", fg="white")
alis_buton.grid(row=5, column=0)

satis_buton = tk.Button(tk_root, text="SAT", command=Hisse_Sat, bg="red", fg="white")
satis_buton.grid(row=5, column=1)

threading.Thread(target=fiyat_guncelle, daemon=True).start()

tk_root.mainloop()
