function updateCharCount() {
  const text = document.getElementById("inputText").value;
  document.getElementById("charCount").innerText = `${text.length} karakter`;
}

function fillExample(text) {
  document.getElementById("inputText").value = text;
  updateCharCount();
}

function scrollToAnalysis() {
  document.getElementById("analysis").scrollIntoView({ behavior: "smooth" });
}

function scrollToAbout() {
  scrollToAnalysis(); // sementara arahkan ke section yang sama
}

const recommendations = {
  "Anxiety": [
    "Coba latihan pernapasan atau relaksasi",
    "Batasi konsumsi kafein dan berita yang memicu cemas",
    "Bicarakan kekhawatiran dengan orang yang dipercaya",
    "Pertimbangkan konsultasi dengan psikolog jika berlanjut"
  ],
  "Depression": [
    "Jaga rutinitas harian sederhana (tidur, makan, aktivitas ringan)",
    "Hubungi teman atau keluarga terdekat untuk bercerita",
    "Konsultasi dengan psikolog atau psikiater untuk penanganan tepat",
    "Hindari mengisolasi diri terlalu lama"
  ],
  "Normal": [
    "Kondisi teks menunjukkan pola yang relatif stabil",
    "Tetap jaga keseimbangan aktivitas dan istirahat",
    "Lanjutkan kebiasaan sehat yang sudah berjalan"
  ],
  "Suicidal": [
    "Segera hubungi layanan darurat kesehatan jiwa (Kemenkes: 119 ext. 8)",
    "Jangan biarkan diri sendirian, hubungi orang terdekat sekarang",
    "Ini adalah indikasi serius — sangat disarankan konsultasi profesional segera",
    "Simpan kontak layanan krisis kesehatan mental di ponsel"
  ]
};

const labelDescriptions = {
  "Anxiety": "Pola teks menunjukkan indikasi kecemasan",
  "Depression": "Pola teks menunjukkan indikasi depresi",
  "Normal": "Pola teks tidak menunjukkan indikasi gangguan signifikan",
  "Suicidal": "Pola teks menunjukkan indikasi risiko serius"
};

async function predict() {
  const text = document.getElementById("inputText").value;
  const labelBadge = document.getElementById("labelBadge");
  const labelDesc = document.getElementById("labelDesc");
  const confidenceBar = document.getElementById("confidenceBar");
  const confidenceValue = document.getElementById("confidenceValue");
  const recommendationBox = document.getElementById("recommendationBox");
  const recommendationList = document.getElementById("recommendationList");
  const statusIcon = document.getElementById("statusIcon");

  if (!text.trim()) {
    labelDesc.innerText = "Tulis teks dulu ya.";
    return;
  }

  labelBadge.innerText = "...";
  labelDesc.innerText = "Memproses...";
  statusIcon.innerText = "⏳";

  try {
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await res.json();

    if (data.error) {
      labelBadge.innerText = "-";
      labelDesc.innerText = data.error;
      statusIcon.innerText = "❌";
      recommendationBox.style.display = "none";
      return;
    }

    const label = data.label;
    const confidence = (data.confidence * 100).toFixed(1);

    labelBadge.innerText = label;
    labelDesc.innerText = labelDescriptions[label] || "";
    confidenceValue.innerText = `${confidence}%`;
    confidenceBar.style.width = `${confidence}%`;
    statusIcon.innerText = "✅";

    const recs = recommendations[label] || [];
    recommendationList.innerHTML = recs.map(r => `<li>${r}</li>`).join("");
    recommendationBox.style.display = recs.length ? "block" : "none";

  } catch (err) {
    labelBadge.innerText = "-";
    labelDesc.innerText = "Gagal menghubungi server. Pastikan backend berjalan.";
    statusIcon.innerText = "❌";
    recommendationBox.style.display = "none";
  }
}