# CurveCraft – Parametric Expression Analyzer

**Transform your intuition into mathematics.**

Draw freehand curves and watch them transform into rigorous mathematical representations, including:

- **Piecewise parametric cubic spline equations**
- **Fourier series approximations** for closed curves
- **Visual comparison tools** between original and reconstructed curves
- **Detailed coefficient tables**

Built with **Tkinter**, **Matplotlib**, **NumPy**, and **SciPy**.

---

## ✨ Features

### 🖌 Interactive Drawing
- Click and drag to draw curves on a Cartesian grid
- Automatic smoothing and arc-length parameterization

### 📐 Parametric Curve Extraction
- Converts drawings into **piecewise cubic splines**
- Displays explicit polynomial expressions for x(t) and y(t)
- Shows parameter intervals and coefficients

### 🔄 Fourier Series Analysis
- Automatic closed-curve detection
- FFT-based computation with adjustable harmonics (3–50)
- Side-by-side visualization of original vs. reconstruction

### 📊 Coefficient Display
- Scrollable Fourier table with cosine and sine coefficients
- Copy functionality for equations and data

### 🎛 Customizable Canvas
- Adjustable X and Y axis ranges
- Quick presets: 1×1, 2×2, π×π, 10×10

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/curvecraft.git
cd curvecraft
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

**Note:** Tkinter comes with standard Python installations.

---

## ▶️ Running the App

```bash
python curvecraft.py
```

---

## 🧪 Usage Tips

- **Draw smoothly** for cleaner splines
- **Close your curve** (end near start) to unlock Fourier analysis
- **Adjust harmonics** to balance accuracy vs. simplicity
- **Use appropriate scale** – switch presets for different contexts

---

## 📦 Dependencies

- Python 3.12
- NumPy
- SciPy
- Matplotlib
- Tkinter (standard library)

```bash
pip install numpy scipy matplotlib
```

---

## 📜 License

MIT License 

---

## 🙌 Acknowledgements

This project started as a high school dream: **deriving equations from curves by sight alone.** Years later, with the right mathematical and technical knowledge, it's finally real.

**Happy curve crafting!** 🎨📐✨

---
