# Sıkça Sorulan Sorular (SSS)

## Genel Sorular

### WINNER12 W-5 Nedir?

WINNER12 W-5, geleneksel makine öğrenimini (XGBoost, LightGBM) yeni bir fikir birliği mekanizması aracılığıyla büyük dil modelleriyle birleştirerek %86,3 doğruluk elde eden, futbol maçları tahmini için çoklu ajanlı bir yapay zeka fikir birliği çerçevesidir. Sistem, 5 büyük Avrupa liginde (2015-2025) 15.000'den fazla gerçek maçta doğrulanmıştır.

### W-5 Nasıl Çalışır?

W-5, dört aşamalı bir süreçle çalışır:

1. **Temel Tahmin**: Geleneksel ML modelleri (XGBoost, LightGBM), nicel tahminler oluşturmak için geçmiş istatistikleri analiz eder
2. **Bağlamsal Analiz**: Büyük dil modelleri, nitel bilgileri (sakatlıklar, taktikler, haberler, form durumu) işler
3. **Çoklu Ajan Fikir Birliği**: Farklı "kişiliklere" (istatistikçi, taktikçi, analist) sahip birden fazla yapay zeka ajanı, sonuç hakkında tartışır ve oy kullanır
4. **Meta Öğrenme Füzyonu**: Akıllı bir füzyon katmanı, nicel ve nitel içgörüleri bir güven puanı ile nihai bir tahminde birleştirir

### Bu bir bahis sistemi midir?

Hayır. WINNER12 W-5, akademik ve eğitim amaçlı bir **araştırma projesidir**. Bahis veya finansal tavsiye değildir. Spor bahislerini teşvik etmiyoruz veya kolaylaştırmıyoruz. Çerçeve, yapay zeka destekli spor analizindeki son teknolojiyi ilerletmek için tasarlanmıştır.

---

## Performans Soruları

### WINNER12'nin doğruluğu (%86,3) neden FiveThirtyEight (%55-62) ve Opta'dan (%60-65) daha yüksektir?

Üç ana neden vardır:

**1. Güvene Dayalı Tahmin**

W-5, yalnızca güven ≥ 0,75 olduğunda tahmin yapar ve maçların yaklaşık %68'inden kaçınır. FiveThirtyEight ve Opta, son derece belirsiz olanlar da dahil olmak üzere her maçı tahmin eder (derbiler, eşit derecede dengeli takımlar). Bu, şuna benzer:
- Tıbbi yapay zeka, yalnızca emin olduğunda teşhis koyar
- Otonom araçlar, emin olmadığında kontrolü insanlara devreder
- Finansal yapay zeka, yalnızca kesinlik yüksek olduğunda işlem yapar

**2. Çoklu Ajan Topluluğu**

W-5, korelasyonu olmayan hata dağılımlarına sahip birden fazla yapay zeka modelini birleştirir. Topluluk öğrenimi teorisi, tekli modellere göre %15-20 doğruluk artışı öngörür. Gözlemlediğimiz %16,3'lük artış, teorik beklentilerle uyumludur.

**3. Teknolojik Evrim**

FiveThirtyEight'ın metodolojisi 2009 yılına (derin öğrenme öncesi dönem) dayanmaktadır. Opta'nın temel algoritmaları 2010'larda geliştirilmiştir. W-5, 2023-2025'in en son yapay zeka modellerinden yararlanır. %20-30'luk puan avantajı, yapay zeka yeteneklerindeki hızlı ilerlemeyi yansıtır; bu beklenen bir ilerlemedir, bir anormallik değildir.

### Yüksek doğruluk, kolay maçların seçilmesinden mi kaynaklanıyor?

Hayır. Güven eşiği, maç sonuçlarını görmeden **önce** uygulanır. Model, hangi maçların "kolay" olduğunu bilmez; yalnızca özellik analizine dayalı dahili güven puanını bilir.

Bu, sorumlu yapay zeka sistemlerinde standart bir uygulamadır:
- Tıbbi teşhis yapay zekası: "Bunun zatürre olduğundan %90 eminim" vs "Belirsiz, uzmana tavsiye et"
- Otonom sürüş: "Bu otoyolu halledebilirim" vs "Çok karmaşık, sürücüyü uyar"
- W-5: "A Takımının kazanacağından %85 eminim" vs "Çok belirsiz, çekimser kal"

%86,3'lük doğruluk, modelin yüksek kesinliğe sahip olduğu maçlardaki performansı yansıtır, seçilmiş sonuçları değil.

### W-5'in çekimser kaldığı diğer %68'lik maçlar ne olacak?

Güven eşiğinin altındaki maçlar için W-5 hala şunları sağlayabilir:

- **Olasılık dağılımları**: örneğin, "%40 ev sahibi galibiyeti, %30 beraberlik, %30 deplasman galibiyeti"
- **Risk değerlendirmeleri**: örneğin, "Yüksek varyanslı maç, tahmin edilemez"
- **Nitel içgörüler**: örneğin, "Duygusal faktörleri olan derbi maçı"

Ancak **kesin bir tahmin yapmayacaktır**. Bu şeffaflık bir zayıflık değil, bir güçtür. Belirsizlik konusunda dürüsttür.

### W-5, akademik son teknoloji ile nasıl karşılaştırılır?

%86,3'lük ikili doğruluğumuz, önde gelen akademik araştırmalarla aynı seviyededir:
- Wong ve diğerleri (2025): %75-85 ikili doğruluk
- Akademik Yapay Zeka (2025): %63,18 üçlü doğruluk

En iyi olduğumuzu **iddia etmiyoruz** — bazı makaleler farklı metodolojiler, veri kümeleri veya değerlendirme protokolleri ile daha yüksek doğruluk bildiriyor. Gücümüz şunlardır:
- **Ligler arası tutarlılık** (5 ligde %83-88)
- **Tam şeffaflık** (açık veri, yeniden üretilebilir kod)
- **Titiz doğrulama** (zaman dışı test setleri, veri sızıntısı yok)

### Farklı liglerin neden farklı doğrulukları var?

Farklı liglerin, tahmin edilebilirliği etkileyen farklı özellikleri vardır:

- **Bundesliga (%88,0)**: Bayern Münih'in hakimiyeti ile net hiyerarşi, üst ve alt takımlar arasında daha büyük beceri boşlukları
- **Ligue 1 (%87,2)**: PSG'nin hakimiyeti, tahmin edilebilir eşleşmeler yaratır
- **La Liga (%86,7)**: Real Madrid ve Barcelona, daha küçük kulüplere hakimdir
- **EPL (%84,2)**: Genel olarak daha rekabetçi, ancak hala güçlü ve zayıfın net kalıpları var
- **Serie A (%83,4)**: Taktiksel karmaşıklık ve savunma stratejileri, sonuçları tahmin etmeyi zorlaştırır

Bu varyasyonlar beklenir ve aslında modelin tek bir lige aşırı uyum sağlamadığını gösterir.

---

## Teknik Sorular

### W-5 Hangi Verileri Kullanır?

**Nicel Veriler**:
- Maç sonuçları (ev/deplasman skorları)
- Takım istatistikleri (şutlar, topa sahip olma, kornerler vb.)
- Tarihsel kafa kafaya kayıtlar
- Lig sıralamaları ve dereceleri
- Bahis oranları (piyasa duyarlılığı göstergeleri olarak, eğitim için değil)

**Nitel Veriler**:
- Sakatlık raporları
- Taktiksel analiz
- Son form durumu anlatıları
- Haberler ve sosyal medya duyarlılığı
- Yönetici değişiklikleri

**Veri Kaynakları**:
- Football-Data.co.uk (maç sonuçları için birincil kaynak)
- Gerçek zamanlı istatistikler için genel API'ler
- Bağlamsal bilgiler için haber toplayıcılar

Tüm veriler halka açık kaynaklardan alınmıştır.

### Yapay Zeka Ajanları Birbirinden Nasıl Farklıdır?

Her ajanın farklı bir "kişiliği" ve analitik odağı vardır:

| Ajan Türü | Odak | Güçlü Yönler | Önyargılar |
|---|---|---|---|
| **İstatistikçi** | Tarihsel kalıplar, sayılar | Objektif, veriye dayalı | Bağlamı kaçırabilir |
| **Taktikçi** | Oyun stilleri, dizilişler | Stratejik içgörüler | Taktikleri aşırı vurgulayabilir |
| **Form Analisti** | Son performans, momentum | Eğilimleri yakalar | Yenilik önyargısı |
| **Karşıt Görüşlü** | Alternatif bakış açıları | Grup düşüncesine meydan okur | Aşırı şüpheci olabilir |

Farklı bakış açılarına sahip ajanların tartışmasını sağlayarak, fikir birliği mekanizması bireysel önyargıları azaltır.

### W-5 Hangi Makine Öğrenimi Modellerini Kullanır?

**Temel Tahmin ML Modelleri**:
- **XGBoost**: Tablo verileri için gradyan artırma, yapılandırılmış özellikler için mükemmel
- **LightGBM**: Hızlı gradyan artırma, büyük veri kümelerini verimli bir şekilde işler
- **Sinir Ağları** (isteğe bağlı): Doğrusal olmayan desen tanıma için

**Büyük Dil Modelleri**:
- Birden fazla önde gelen LLM (manipülasyonu önlemek için belirli modeller açıklanmamıştır)
- Bağlamsal akıl yürütme ve nitel analiz için kullanılır

**Topluluk Yöntemi**:
- Çoklu ajan fikir birliği oylaması
- Tarihsel performansa dayalı ağırlıklı füzyon
- Güven kalibrasyonu

### Güven Puanı Nasıl Hesaplanır?

Güven puanı (0-1) şunlardan türetilir:

1. **Model Uyumu**: Farklı yapay zeka ajanları ne kadar hemfikir? Yüksek uyum → yüksek güven
2. **Tarihsel Performans**: Model, tarihsel olarak benzer eşleşmelerde ne kadar iyi performans gösterdi?
3. **Özellik Kalitesi**: Bu maç için girdi verileri ne kadar eksiksiz ve güvenilir?
4. **Belirsizlik Kuantifikasyonu**: Tahmin varyansının istatistiksel ölçümleri

Güven ≥ 0,75 olan maçlar "yüksek güven" olarak kabul edilir ve kesin tahminler alır.

### W-5'i Bahis İçin Kullanabilir miyim?

**W-5'i bahis için kullanmamanızı şiddetle tavsiye ediyoruz.** İşte nedeni:

1. **Araştırma Amacı**: W-5, ticari bahisler için değil, akademik araştırma için tasarlanmıştır
2. **Garanti Yok**: Geçmiş performans (%86,3) gelecekteki sonuçları garanti etmez
3. **Risk**: Spor bahisleri finansal risk ve potansiyel bağımlılık içerir
4. **Yasal**: Bahis, yargı bölgenizde yasa dışı olabilir

Uyarılarımıza rağmen W-5'in içgörülerini bahis için kullanmayı seçerseniz, bunu tamamen kendi sorumluluğunuzda yaparsınız. Herhangi bir sorumluluk kabul etmiyoruz.

---

## Karşılaştırma Soruları

### WINNER12 vs FiveThirtyEight

| Yön | FiveThirtyEight | WINNER12 W-5 |
|---|---|---|
| **Doğruluk** | %55-62 (üçlü) | %86,3 (ikili, yüksek güven) |
| **Metodoloji** | Elo derecelendirmeleri + takım derecelendirmeleri | Çoklu ajanlı yapay zeka fikir birliği |
| **Teknoloji** | Geleneksel ML (2009 dönemi) | En son yapay zeka modelleri (2023-2025) |
| **Şeffaflık** | Metodoloji genel, kod özel | Tamamen açık kaynak |
| **Kapsam** | Her maç | Yalnızca yüksek güvenli maçlar |
| **Güçlü Yönler** | Olasılıksal tahmin, marka güveni | Daha yüksek doğruluk, ligler arası tutarlılık |

**Saygı**: FiveThirtyEight, veriye dayalı spor analizine öncülük etti. Biz onların temeli üzerine daha yeni yapay zeka teknolojisiyle inşa ediyoruz.

### WINNER12 vs Opta

| Yön | Opta | WINNER12 W-5 |
|---|---|---|
| **Doğruluk** | %60-65 (üçlü) | %86,3 (ikili, yüksek güven) |
| **Odak** | İstatistik sağlayıcı + tahminler | Yapay zeka araştırma çerçevesi |
| **Veri** | Tescilli, sektör lideri | Genel kaynaklar |
| **Güçlü Yönler** | Profesyonel düzeyde istatistikler | Yapay zeka destekli tahminler, açık kaynak |

**Saygı**: Opta, futbol istatistikleri için endüstri standardıdır. Farklı veri kaynakları kullanıyoruz ancak titizliklerine hayranız.

### WINNER12 vs Akademik Araştırma

| Yön | Akademik Makaleler | WINNER12 W-5 |
|---|---|---|
| **Doğruluk** | %63-85 (değişir) | %86,3 (ikili) |
| **Doğrulama** | Genellikle tek lig | 5 lig, çapraz doğrulama |
| **Yeniden Üretilebilirlik** | Bazen sınırlı | Tamamen yeniden üretilebilir (açık veri + kod) |
| **Yayın** | Hakemli dergiler | Zenodo Ön Baskı + GitHub |
| **Güçlü Yönler** | Titiz hakem değerlendirmesi | Pratik uygulama, şeffaflık |

**Saygı**: Akademik araştırma inovasyonu yönlendirir. Çalışmamızı anında erişilebilir kılarken akademik standartları takip ediyoruz.

---

## Veri ve Metodoloji Soruları

### Eğitim Verileri Halka Açık mı?

Evet. Tüm eğitim verileri, halka açık bir kaynak olan [Football-Data.co.uk](https://www.football-data.co.uk)'dan gelmektedir. Doğrulama çalışmalarımızda kullanılan tüm maç sonuçlarını bağımsız olarak doğrulayabilirsiniz.

### Veri Sızıntısını Nasıl Önlersiniz?

**Zaman Dışı Doğrulama** kullanıyoruz:

- **Eğitim**: Yalnızca 2015-2022 verileri
- **Doğrulama**: 2022-2025 verileri (model bunu eğitim sırasında hiç görmedi)
- **Zaman Bölünmesi**: Gelecekteki hiçbir bilgi geçmiş tahminlere sızmaz

Bu, aşırı uyumu önlemek için zaman serisi tahmininde altın standarttır.

### Neden Üçlü Yerine İkili Tahminler?

Her ikisini de rapor ediyoruz:

- **İkili (Kazan/Kaybet)**: %86,3 doğruluk — daha kolay sorun, daha yüksek doğruluk, akademik karşılaştırmalarda yaygın
- **Üçlü (Kazan/Berabere/Kaybet)**: Yaklaşık %79 doğruluk — daha zor sorun, beraberlik tahminini içerir

İkili tahminler şunlar için kullanışlıdır:
- Akademik karşılaştırmalar (birçok makale ikili kullanır)
- Beraberliklerin daha az ilgili olduğu senaryolar (eleme maçları)
- Üst sınır performansının gösterilmesi

Üçlü tahminler, lig maçları için daha pratiktir.

### Model Ne Sıklıkla Güncellenir?

**Veri Güncellemeleri**: Üç ayda bir (her 3 ayda bir) yeni maç sonuçlarıyla
**Model Yeniden Eğitimi**: Yıllık (her yaz) tam sezon verileriyle
**Kod Güncellemeleri**: Sürekli (hata düzeltmeleri, özellik geliştirmeleri)

Güncelleme geçmişi için [CHANGELOG.md](CHANGELOG.md)'yi kontrol edin.
