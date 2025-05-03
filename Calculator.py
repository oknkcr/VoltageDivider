import tkinter as tk
from tkinter import ttk
import math
from tkinter import messagebox
import time
import sys
import os

class VoltageCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Direnç Bölücü Hesaplayıcı")
        self.root.geometry("550x880")
        
        # Minimum boyut ayarla
        self.root.minsize(450, 600)
        
        # Ekran ölçeklendirme için ağırlık tanımlamaları
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Dark tema renkleri
        self.colors = {
            "bg_dark": "#1e1e1e",
            "bg_medium": "#2d2d2d",
            "bg_light": "#3c3c3c",
            "input_bg": "#cccccc",     # Text input arka plan rengi (açık gri)
            "input_text": "#000000",   # Text input yazı rengi (siyah)
            "text": "#ffffff",
            "text_muted": "#aaaaaa",
            "accent": "#007acc",       # Mavi vurgu rengi
            "accent_hover": "#1c97ea",
            "button_bg": "#4a6fa5",    # Buton arka plan (mavi)
            "button_text": "#ffffff",  # Buton metni (beyaz)
            "button_hover": "#5f86bf", # Buton hover hali
            "control_bg": "#555555",   # Kontrol butonları arka plan
            "control_text": "#ffffff", # Kontrol butonları metin rengi
            "control_hover": "#777777",# Kontrol butonları hover hali
            "success": "#4caf50",      # Yeşil
            "warning": "#ff9800",      # Turuncu
            "error": "#f44336",        # Kırmızı
            "separator": "#555555"
        }
        
        # Standart direnç değerleri (E24 serisi)
        self.standard_resistors = [
            1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 
            3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1, 10
        ]
        self.r1_index = 0
        self.r2_index = 0
        
        # Pencere yeniden boyutlandırma kontrolü için değişkenler
        self.resize_timer_id = None
        self.is_dragging = False
        
        # Dark tema uygula
        self.apply_dark_theme()
        
        # Widget'ları oluştur
        self.create_widgets()
        
    def apply_dark_theme(self):
        self.root.configure(bg=self.colors["bg_dark"])
        
        style = ttk.Style()
        
        # Ana stil tanımları
        style.configure("TFrame", background=self.colors["bg_dark"])
        style.configure("TLabel", 
            background=self.colors["bg_dark"], 
            foreground=self.colors["text"],
            font=("Segoe UI", 10)
        )
        
        # Buton stilleri - Daha kontrast renkler
        style.configure("TButton", 
            background=self.colors["button_bg"],
            foreground="#000000",  # Buton yazı rengi siyah olarak değiştirildi
            font=("Segoe UI", 12, "bold"),  # Puntoyu artırıldı
            borderwidth=1,
            focusthickness=3,
            relief="raised"
        )
        style.map("TButton",
            background=[("active", self.colors["button_hover"])],
            foreground=[("active", "#000000")],  # Hover durumunda da siyah kalması için
            relief=[("pressed", "sunken"), ("!pressed", "raised")]
        )
        
        # Giriş stilleri - Açık renk arka plan ve koyu metin
        style.configure("TEntry", 
            fieldbackground=self.colors["input_bg"],
            foreground=self.colors["input_text"],
            borderwidth=1,
            font=("Segoe UI", 12),  # Puntoyu artırıldı
            padding=8
        )
        
        # Özel Frame stilleri
        style.configure("Card.TFrame", 
            background=self.colors["bg_medium"],
            relief="raised", 
            borderwidth=1
        )
        
        style.configure("Info.TFrame", 
            background=self.colors["bg_light"],
            relief="flat"
        )
        
        # Özel Label stilleri  
        style.configure("Title.TLabel",
            font=("Segoe UI", 18, "bold"),  # Puntoyu artırıldı
            foreground=self.colors["text"],
            background=self.colors["bg_dark"]
        )
        
        style.configure("Subtitle.TLabel",
            font=("Segoe UI", 14, "bold"),  # Puntoyu artırıldı
            foreground=self.colors["accent"],
            background=self.colors["bg_dark"]
        )
        
        style.configure("Value.TLabel",
            font=("Segoe UI", 14),  # Puntoyu artırıldı
            foreground=self.colors["text"],
            background=self.colors["bg_medium"]
        )
        
        # Kontrol butonları için özel stil
        style.configure("Control.TButton",
            font=("Segoe UI", 13, "bold"),  # Puntoyu artırıldı
            background=self.colors["control_bg"],
            foreground="#000000",  # Yazı rengi siyah olarak değiştirildi
            borderwidth=1,
            relief="raised"
        )
        style.map("Control.TButton",
            background=[("active", self.colors["control_hover"])],
            foreground=[("active", "#000000")],  # Hover durumunda da siyah kalması için
            relief=[("pressed", "sunken"), ("!pressed", "raised")]
        )
        
    def create_widgets(self):
        # Ana çerçeve - pack yerine grid kullanarak ölçeklendirme desteği
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Ana frame'i ölçeklendirme için yapılandır
        main_frame.grid_columnconfigure(0, weight=1)
        
        current_row = 0
        
        # Başlık
        title_label = ttk.Label(
            main_frame, 
            text="Direnç Bölücü Hesaplayıcı",
            style="Title.TLabel"
        )
        title_label.grid(row=current_row, column=0, pady=(0, 20))
        current_row += 1
        
        # Referans voltaj
        ref_frame = ttk.Frame(main_frame)
        ref_frame.grid(row=current_row, column=0, sticky="ew", pady=10)
        ref_frame.grid_columnconfigure(1, weight=1)  # Entry'nin genişlemesi için
        
        # Label için farklı bir arka plan rengi tanımla
        ttk.Label(ref_frame, text="Ref. Voltaj:", background=self.colors["bg_dark"]).grid(row=0, column=0, padx=(0, 10))
        self.ref_voltage = tk.StringVar(value="0.768")
        
        # Text Entry için standart ttk.Entry yerine özel bir Entry widget'ı 
        ref_entry = ttk.Entry(ref_frame, textvariable=self.ref_voltage, justify="center")
        ref_entry.grid(row=0, column=1, sticky="ew")
        
        ttk.Label(ref_frame, text="V", background=self.colors["bg_dark"]).grid(row=0, column=2, padx=(10, 0))
        current_row += 1
        
        # Hesaplama açıklaması
        info_frame = ttk.Frame(main_frame, padding=10, style="Info.TFrame")
        info_frame.grid(row=current_row, column=0, sticky="ew", pady=15)
        info_frame.grid_columnconfigure(0, weight=1)
        
        info_label = ttk.Label(
            info_frame, 
            text="Aşağıdaki herhangi iki girişi doldurun ve 3. değer için hesaplaya tıklayın",
            anchor="center",
            wraplength=480,
            background=self.colors["bg_light"],
            foreground=self.colors["text"]
        )
        info_label.grid(row=0, column=0)
        current_row += 1
        
        # Girişler çerçevesi - hepsini içerecek
        entries_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        entries_frame.grid(row=current_row, column=0, sticky="ew", pady=10)
        entries_frame.grid_columnconfigure(1, weight=1)  # Entry'lerin genişlemesi için
        entries_row = 0
        
        # R1 girişi
        ttk.Label(entries_frame, text="R1:", background=self.colors["bg_medium"], font=("Segoe UI", 12)).grid(row=entries_row, column=0, padx=(0, 10), sticky="w")
        self.r1_value = tk.StringVar()
        r1_entry = ttk.Entry(entries_frame, textvariable=self.r1_value, justify="center")
        r1_entry.grid(row=entries_row, column=1, sticky="ew", padx=5)
        ttk.Label(entries_frame, text="kΩ", background=self.colors["bg_medium"], font=("Segoe UI", 12)).grid(row=entries_row, column=2, padx=(5, 10))
        r1_calc_btn = ttk.Button(entries_frame, text="Hesapla", command=lambda: self.calculate("r1"))
        r1_calc_btn.grid(row=entries_row, column=3)
        entries_row += 1
        
        # Ayırıcı çizgi
        separator1 = ttk.Separator(entries_frame, orient="horizontal")
        separator1.grid(row=entries_row, column=0, columnspan=4, sticky="ew", pady=10)
        entries_row += 1
        
        # R2 girişi
        ttk.Label(entries_frame, text="R2:", background=self.colors["bg_medium"], font=("Segoe UI", 12)).grid(row=entries_row, column=0, padx=(0, 10), sticky="w")
        self.r2_value = tk.StringVar()
        r2_entry = ttk.Entry(entries_frame, textvariable=self.r2_value, justify="center")
        r2_entry.grid(row=entries_row, column=1, sticky="ew", padx=5)
        ttk.Label(entries_frame, text="kΩ", background=self.colors["bg_medium"], font=("Segoe UI", 12)).grid(row=entries_row, column=2, padx=(5, 10))
        r2_calc_btn = ttk.Button(entries_frame, text="Hesapla", command=lambda: self.calculate("r2"))
        r2_calc_btn.grid(row=entries_row, column=3)
        entries_row += 1
        
        # Ayırıcı çizgi
        separator2 = ttk.Separator(entries_frame, orient="horizontal")
        separator2.grid(row=entries_row, column=0, columnspan=4, sticky="ew", pady=10)
        entries_row += 1
        
        # Çıkış voltajı girişi
        ttk.Label(entries_frame, text="Çıkış V:", background=self.colors["bg_medium"], font=("Segoe UI", 12)).grid(row=entries_row, column=0, padx=(0, 10), sticky="w")
        self.out_voltage = tk.StringVar()
        out_entry = ttk.Entry(entries_frame, textvariable=self.out_voltage, justify="center")
        out_entry.grid(row=entries_row, column=1, sticky="ew", padx=5)
        ttk.Label(entries_frame, text="V", background=self.colors["bg_medium"], font=("Segoe UI", 12)).grid(row=entries_row, column=2, padx=(5, 10))
        out_calc_btn = ttk.Button(entries_frame, text="Hesapla", command=lambda: self.calculate("out"))
        out_calc_btn.grid(row=entries_row, column=3)
        current_row += 1
        
        # Entry widget'larının içindeki metni siyah yapmak için doğrudan stil atama
        for entry in [ref_entry, r1_entry, r2_entry, out_entry]:
            entry.config(style="TEntry")
        
        # Standart Direnç Değerleri başlığı
        std_label = ttk.Label(
            main_frame, 
            text="Standart Direnç Değerleri ile Çıkış",
            style="Subtitle.TLabel"
        )
        std_label.grid(row=current_row, column=0, pady=(20, 10))
        current_row += 1
        
        # Standart değerler çerçevesi
        std_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        std_frame.grid(row=current_row, column=0, sticky="ew", pady=10)
        std_frame.grid_columnconfigure(0, weight=1)  # İçeriğin ortalanması için
        std_row = 0
        
        # Çıkış Voltajı gösterimi
        out_display_frame = ttk.Frame(std_frame, padding=10)
        out_display_frame.grid(row=std_row, column=0, sticky="ew", pady=5)
        out_display_frame.grid_columnconfigure(0, weight=1)  # İçeriğin ortalanması için
        
        ttk.Label(
            out_display_frame,
            text="Çıkış Voltajı",
            foreground=self.colors["accent"],
            background=self.colors["bg_medium"],
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=0)
        
        self.out_display = ttk.Label(
            out_display_frame,
            text="0.000 V",
            style="Value.TLabel",
            font=("Segoe UI", 16, "bold")
        )
        self.out_display.grid(row=1, column=0, pady=5)
        std_row += 1
        
        # Direnç seçicileri çerçevesi
        resistors_frame = ttk.Frame(std_frame, padding=5)
        resistors_frame.grid(row=std_row, column=0, sticky="ew", pady=10)
        resistors_frame.grid_columnconfigure(0, weight=1)
        resistors_frame.grid_columnconfigure(1, weight=1)
        
        # R1 seçimi
        r1_select_frame = ttk.Frame(resistors_frame, padding=10, style="Card.TFrame")
        r1_select_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        r1_select_frame.grid_columnconfigure(0, weight=1)  # İçeriğin ortalanması için
        
        ttk.Label(
            r1_select_frame,
            text="Direnç (R1)",
            foreground=self.colors["accent"],
            background=self.colors["bg_medium"],
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0)
        
        r1_select_buttons = ttk.Frame(r1_select_frame, style="Card.TFrame")
        r1_select_buttons.grid(row=1, column=0, pady=5)
        
        ttk.Button(
            r1_select_buttons, 
            text="<", 
            width=3, 
            command=self.decrease_r1,
            style="Control.TButton"
        ).grid(row=0, column=0, padx=5)
        
        self.r1_display = ttk.Label(
            r1_select_buttons,
            text=f"{self.standard_resistors[self.r1_index]} kΩ",
            style="Value.TLabel",
            width=8
        )
        self.r1_display.grid(row=0, column=1, padx=10)
        
        ttk.Button(
            r1_select_buttons, 
            text=">", 
            width=3, 
            command=self.increase_r1,
            style="Control.TButton"
        ).grid(row=0, column=2, padx=5)
        
        # R2 seçimi
        r2_select_frame = ttk.Frame(resistors_frame, padding=10, style="Card.TFrame")
        r2_select_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        r2_select_frame.grid_columnconfigure(0, weight=1)  # İçeriğin ortalanması için
        
        ttk.Label(
            r2_select_frame,
            text="Direnç (R2)",
            foreground=self.colors["accent"],
            background=self.colors["bg_medium"],
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0)
        
        r2_select_buttons = ttk.Frame(r2_select_frame, style="Card.TFrame")
        r2_select_buttons.grid(row=1, column=0, pady=5)
        
        ttk.Button(
            r2_select_buttons,
            text="<",
            width=3,
            command=self.decrease_r2,
            style="Control.TButton"
        ).grid(row=0, column=0, padx=5)
        
        self.r2_display = ttk.Label(
            r2_select_buttons,
            text=f"{self.standard_resistors[self.r2_index]} kΩ",
            style="Value.TLabel",
            width=8
        )
        self.r2_display.grid(row=0, column=1, padx=10)
        
        ttk.Button(
            r2_select_buttons, 
            text=">", 
            width=3, 
            command=self.increase_r2,
            style="Control.TButton"
        ).grid(row=0, column=2, padx=5)
        std_row += 1
        
        # Standart değerlerle hesaplama butonu
        std_calc_btn = ttk.Button(
            std_frame, 
            text="Standart Değerlerle Hesapla", 
            command=self.calculate_with_standard_values
        )
        std_calc_btn.grid(row=std_row, column=0, pady=10)
        current_row += 1
        
        # Bilgi ve telif hakkı
        footer_label = ttk.Label(
            main_frame, 
            text="Copyright © 2025 Okan Kocer",
            foreground=self.colors["text_muted"],
            background=self.colors["bg_dark"],
            font=("Segoe UI", 8)
        )
        footer_label.grid(row=current_row, column=0, pady=(20, 0))
        
        # Pencere events'larını bağla
        self.root.bind("<Configure>", self.on_configure)
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
    
    def start_move(self, event):
        """Fare ile sürükleme başladığında çağrılır"""
        # Sürükleme işlemi başladı
        self.is_dragging = True
    
    def stop_move(self, event):
        """Fare ile sürükleme bittiğinde çağrılır"""
        # Sürükleme işlemi bitti, resize'ı tetikle
        self.is_dragging = False
        # Eğer bekleyen bir resize timer varsa iptal et ve hemen tetikle
        if self.resize_timer_id:
            self.root.after_cancel(self.resize_timer_id)
        self.resize_ui()
    
    def on_configure(self, event):
        """Pencere boyutu veya pozisyonu değiştiğinde çağrılır"""
        # Sürükleme esnasında resize işlemini yapma
        if self.is_dragging:
            return
            
        # Eğer bekleyen bir timer varsa iptal et
        if self.resize_timer_id:
            self.root.after_cancel(self.resize_timer_id)
            
        # 200ms sonra resize işlemini gerçekleştir
        # Bu şekilde hızlı resize işlemleri sırasında sürekli tetiklenmeyecek
        self.resize_timer_id = self.root.after(200, self.resize_ui)
    
    def resize_ui(self):
        """UI öğelerinin boyutlarını yeniden ayarlar"""
        # Reset timer ID
        self.resize_timer_id = None
        
        # Pencere boyutlarını al
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Yazı tipi boyutunu pencere boyutuna göre ölçeklendirme
        if width < 500:
            base_font_size = 11  # Baz font boyutu artırıldı
        elif width < 700:
            base_font_size = 12  # Baz font boyutu artırıldı
        else:
            base_font_size = 13  # Baz font boyutu artırıldı
        
        style = ttk.Style()
        
        # Yazı tipi boyutlarını güncelle
        style.configure("TLabel", font=("Segoe UI", base_font_size))
        style.configure("TButton", font=("Segoe UI", base_font_size, "bold"), foreground="#000000")
        style.configure("TEntry", font=("Segoe UI", base_font_size))
        
        style.configure("Title.TLabel", font=("Segoe UI", base_font_size + 6, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", base_font_size + 3, "bold"))
        style.configure("Value.TLabel", font=("Segoe UI", base_font_size + 2))
        style.configure("Control.TButton", font=("Segoe UI", base_font_size + 1, "bold"), foreground="#000000")
    
    def calculate(self, calculate_for):
        try:
            ref_v = float(self.ref_voltage.get())
            
            if calculate_for == "r1":
                if self.r2_value.get() and self.out_voltage.get():
                    r2 = float(self.r2_value.get())
                    out_v = float(self.out_voltage.get())
                    
                    # Çıkış değerinin referanstan küçük olmaması kontrolü
                    if out_v < ref_v:
                        messagebox.showwarning("Değer Hatası", "Çıkış gerilimi, referans geriliminden küçük olamaz!")
                        return
                    
                    # R1 hesaplama formülü (yükseltici devre için): R1 = R2 / (Vout/Vref - 1)
                    if out_v == ref_v:
                        self.r1_value.set("Sonsuz")
                    else:
                        r1 = r2 / (out_v/ref_v - 1)
                        self.r1_value.set(f"{r1:.2f}")
                else:
                    self.r1_value.set("R2 ve Çıkış V gerekli")
            
            elif calculate_for == "r2":
                if self.r1_value.get() and self.out_voltage.get():
                    r1 = float(self.r1_value.get())
                    out_v = float(self.out_voltage.get())
                    
                    # Çıkış değerinin referanstan küçük olmaması kontrolü
                    if out_v < ref_v:
                        messagebox.showwarning("Değer Hatası", "Çıkış gerilimi, referans geriliminden küçük olamaz!")
                        return
                    
                    # R2 hesaplama formülü (yükseltici devre için): R2 = R1 * (Vout/Vref - 1)
                    if out_v == ref_v:
                        self.r2_value.set("0")
                    else:
                        r2 = r1 * (out_v/ref_v - 1)
                        self.r2_value.set(f"{r2:.2f}")
                else:
                    self.r2_value.set("R1 ve Çıkış V gerekli")
            
            elif calculate_for == "out":
                if self.r1_value.get() and self.r2_value.get():
                    r1 = float(self.r1_value.get())
                    r2 = float(self.r2_value.get())
                    
                    # Çıkış voltajı hesaplama formülü (yükseltici devre için): Vout = Vref * (1 + R2/R1)
                    if r1 == 0:
                        self.out_voltage.set("Sıfıra bölme hatası")
                    else:
                        out_v = ref_v * (1 + r2/r1)
                        self.out_voltage.set(f"{out_v:.4f}")
                        self.out_display.config(text=f"{out_v:.4f} V")
                else:
                    self.out_voltage.set("R1 ve R2 gerekli")
        
        except ValueError:
            if calculate_for == "r1":
                self.r1_value.set("Geçersiz değerler")
            elif calculate_for == "r2":
                self.r2_value.set("Geçersiz değerler")
            elif calculate_for == "out":
                self.out_voltage.set("Geçersiz değerler")
    
    def increase_r1(self):
        # Bir sonraki standart direnç değerine geç
        self.r1_index = (self.r1_index + 1) % len(self.standard_resistors)
        self.r1_display.config(text=f"{self.standard_resistors[self.r1_index]} kΩ")
        self.calculate_with_standard_values()
    
    def decrease_r1(self):
        # Bir önceki standart direnç değerine geç
        self.r1_index = (self.r1_index - 1) % len(self.standard_resistors)
        self.r1_display.config(text=f"{self.standard_resistors[self.r1_index]} kΩ")
        self.calculate_with_standard_values()
    
    def increase_r2(self):
        # Bir sonraki standart direnç değerine geç
        self.r2_index = (self.r2_index + 1) % len(self.standard_resistors)
        self.r2_display.config(text=f"{self.standard_resistors[self.r2_index]} kΩ")
        self.calculate_with_standard_values()
    
    def decrease_r2(self):
        # Bir önceki standart direnç değerine geç
        self.r2_index = (self.r2_index - 1) % len(self.standard_resistors)
        self.r2_display.config(text=f"{self.standard_resistors[self.r2_index]} kΩ")
        self.calculate_with_standard_values()
    
    def calculate_with_standard_values(self):
        try:
            ref_v = float(self.ref_voltage.get())
            r1 = self.standard_resistors[self.r1_index]
            r2 = self.standard_resistors[self.r2_index]
            
            # Çıkış voltajı hesaplama (yükseltici devre için)
            out_v = ref_v * (1 + r2/r1)
            
            # Göstergeyi güncelle
            self.out_display.config(text=f"{out_v:.4f} V")
            
            # Ana hesaplama alanlarını da güncelle
            self.r1_value.set(f"{r1}")
            self.r2_value.set(f"{r2}")
            self.out_voltage.set(f"{out_v:.4f}")
            
        except (ValueError, ZeroDivisionError):
            self.out_display.config(text="Hata")

def main():
    # Lisans kontrolünü kaldırdık, direkt uygulamayı başlat
    try:
        root = tk.Tk()
        app = VoltageCalculator(root)
        root.mainloop()
    except Exception as e:
        # Hata mesajı göstermek için basit bir pencere
        error_root = tk.Tk()
        error_root.withdraw()
        messagebox.showerror("Hata", f"Uygulama başlatılırken bir hata oluştu:\n{str(e)}")
        error_root.destroy()
        sys.exit(1)

if __name__ == "__main__":
    main()
