import cv2
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


#  RENKLİ GÖRÜNTÜLERDE HISTOGRAM EŞİTLEME (HER KANALA AYRI UYGULANIR)
def apply_equalization(img):
    # B, G, R kanallarına ayırma
    b, g, r = cv2.split(img)

    # Her kanala histogram eşitleme
    b_eq = cv2.equalizeHist(b)
    g_eq = cv2.equalizeHist(g)
    r_eq = cv2.equalizeHist(r)

    # Kanalları geri birleştirme
    return cv2.merge((b_eq, g_eq, r_eq))

#  RENKLİ CLAHE UYGULAMASI (DOĞAL VE KALİTELİ SONUÇ)
def apply_CLAHE(img):
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

    b, g, r = cv2.split(img)

    b_cl = clahe.apply(b)
    g_cl = clahe.apply(g)
    r_cl = clahe.apply(r)

    return cv2.merge((b_cl, g_cl, r_cl))

#  ANA UYGULAMA SINIFI
class HistogramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Histogram ve Kontrast İyileştirme")
        self.root.configure(bg="#222222")

        self.original_img = None
        self.processed_img = None

        # ÜST MENÜ
        top = tk.Frame(root, bg="#222222")
        top.pack(pady=10)

        tk.Button(top, text="Resim Seç", bg="#333", fg="white",
                  font=("Arial", 11), command=self.load_image)\
            .pack(side="left", padx=5)

        tk.Button(top, text="İşlemi Uygula", bg="#444", fg="white",
                  font=("Arial", 11), command=self.apply_filter)\
            .pack(side="left", padx=5)

        tk.Button(top, text="Kaydet", bg="#555", fg="white",
                  font=("Arial", 11), command=self.save_image)\
            .pack(side="left", padx=5)

        tk.Label(top, text=" Filtre:", fg="white", bg="#222",
                 font=("Arial", 11)).pack(side="left")

        self.filter_var = tk.StringVar(value="CLAHE")
        ttk.Combobox(top, textvariable=self.filter_var,
                     values=["CLAHE", "Histogram Equalization"],
                     width=25).pack(side="left", padx=10)

        #ANA GÖRSEL ALANI
        self.canvas = tk.Canvas(root, bg="#111",
                                width=1200, height=700, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

    #--------------------------------------------------------------
    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Görüntü Dosyaları",
                        "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
        )
        if not file_path:
            return

        self.original_img = cv2.imread(file_path)
        self.processed_img = None
        self.show_images()

    #--------------------------------------------------------------
    def apply_filter(self):
        if self.original_img is None:
            return

        img = self.original_img.copy()
        choice = self.filter_var.get()

        if choice == "CLAHE":
            self.processed_img = apply_CLAHE(img)

        elif choice == "Histogram Equalization":
            self.processed_img = apply_equalization(img)

        self.show_images()

    #---------------------------------------------------------------
    def save_image(self):
        if self.processed_img is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
        )
        if file_path:
            cv2.imwrite(file_path, self.processed_img)

    #  RESİMLERİ GÖSTERME + PSNR/SSIM YAZDIRMA
    def show_images(self):
        self.canvas.delete("all")

        if self.original_img is None:
            return

        # Canvas boyutlarını alma
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        half_w = canvas_w // 2 - 20

        #ORİJİNAL
        orig = self.resize_fit_for_canvas(self.original_img, half_w, canvas_h - 40)
        orig_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)))

        self.canvas.create_image(10, 20, image=orig_tk, anchor="nw")
        self.canvas.orig_img = orig_tk

        #İŞLENMİŞ + METRİKLER
        if self.processed_img is not None:
            proc = self.resize_fit_for_canvas(self.processed_img, half_w, canvas_h - 40)
            proc_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(proc, cv2.COLOR_BGR2RGB)))

            self.canvas.create_image(half_w + 30, 20, image=proc_tk, anchor="nw")
            self.canvas.proc_img = proc_tk

            # PSNR ve SSIM hesaplama
            psnr = peak_signal_noise_ratio(orig, proc)
            ssim = structural_similarity(orig, proc, channel_axis=-1)

            # ALTTA METİN OLARAK GÖSTERME
            self.canvas.create_text(
                half_w + 30,
                proc.shape[0] + 40,
                anchor="nw",
                fill="white",
                font=("Arial", 13, "bold"),
                text=f"PSNR: {psnr:.2f}   |   SSIM: {ssim:.4f}"
            )

    #-----------------------------------------------------
    def resize_fit_for_canvas(self, img, max_w, max_h):
        h, w = img.shape[:2]
        scale = min(max_w / w, max_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)



#  PROGRAM BAŞLANGICI
root = tk.Tk()
app = HistogramApp(root)
root.mainloop()
