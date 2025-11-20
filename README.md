Görüntü Histogramı ve Kontrast Geliştirme
X-Ray görüntülerinde histogram analizi ve kontrast iyileştirme

Bu proje, göğüs röntgeni görüntülerinde histogram analizi ve kontrast artırma işlemleri yapmayı amaçlar.
Uygulama:
- Histogram Equalization
- CLAHE (Contrast Limited Adaptive Histogram Equalization)
metotlarını kullanarak görüntü kalitesini iyileştirir.

Tkinter tabanlı grafik arayüz (GUI) sayesinde kullanıcı:
- Görüntü seçebilir
- İstediği filtreyi uygulayabilir
- Orijinal ve işlenmiş görüntüyü yan yana görebilir
- Sonucu kaydedebilir

Kullanılan Yöntemler:
- Histogram Equalization
- CLAHE
- PSNR (Peak Signal-to-Noise Ratio)
- SSIM (Structural Similarity Index Measure)

DEMO GÖRSELLER:
<p align="center">
  <p>1.görsel: CLAHE<p>
  <img src="img1.png" width="55%">
  
  <br>
  <p>2.görsel: Histogram Equalization<p> 
  <br>
  <img src="img2.png" width="55%">
</p>


KURULUM:
Ortamı oluştur: python -m venv venv
Ortamı aktif et: 
Windows:venv\Scripts\activate
Mac/Linux:source venv/bin/activate
pip install -r requirements.txt
python image_app.py

goruntu-histogrami-ve-kontrast-gelistirme:
-image_app.py
-requirements.txt
-README.md
-.gitignore



  


