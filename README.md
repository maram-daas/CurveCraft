# CurveCraft – Parametric Expression Analyzer

CurveCraft is an interactive Python application that allows users to **draw freehand curves** and automatically transform them into **mathematical representations**, including:

- Piecewise **parametric cubic spline equations**
- **Fourier series approximations** for closed curves
- Visual comparison between original and reconstructed curves
- A detailed, scrollable **Fourier coefficient table**

Built with **Tkinter**, **Matplotlib**, **NumPy**, and **SciPy**, CurveCraft is designed for learning, experimentation, and mathematical visualization.

---

## ✨ Features

### 🖌 Interactive Drawing
- Click and drag to draw curves directly on a Cartesian grid
- Release to finish drawing
- Automatic smoothing and arc-length parameterization

### 📐 Parametric Curve Extraction
- Converts drawings into **piecewise cubic splines**
- Displays explicit polynomial expressions for each segment:
  - \( x(t) \)
  - \( y(t) \)
- Shows parameter intervals and coefficients

### 🔄 Fourier Series Analysis (Closed Curves)
- Automatically detects closed curves
- Computes Fourier series using FFT
- Adjustable number of harmonics (3–50)
- Visual comparison:
  - Original spline
  - Fourier approximation

### 📊 Fourier Coefficient Table
- Scrollable table displaying:
  - Cosine and sine coefficients for x(t) and y(t)

### 🎛 Customizable Canvas
- Adjustable X and Y ranges
- Preset grid sizes (1×1, 2×2, π×π, 10×10)
---

## 🧠 How It Works

1. User draws a curve on the canvas
2. Points are smoothed and re-parameterized by arc length
3. Cubic splines are fit to x(t) and y(t)
4. If the curve is closed:
   - FFT is applied
   - Fourier coefficients are extracted
   - Series reconstruction is displayed

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/curvecraft.git
cd curvecraft
```
2. Install dependencies
Copy code
```bash
pip install -r requirements.txt
```
Note: Tkinter is included with most standard Python installations.

▶ Running the App
```bash
python CurveCraft.py
```

🧪 Controls & Tips

Draw slowly for smoother splines

Close your curve to unlock Fourier mode

Increase harmonics for better Fourier accuracy

Use presets to quickly change scale

Click Copy All to export equations

📦 Dependencies

Python 3.12

NumPy

SciPy

Matplotlib

Tkinter (standard library)

📜 License
This project is released under the MIT License.

🙌 Acknowledgements
Deriving functions expression just by their visual representations has always been an idea i wanted to apply in real since highschool, now i finally got the mathematical and technical knowledge i made this project a reality.

Happy curve crafting! 🎨📐
