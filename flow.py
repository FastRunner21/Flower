<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pointillism Flower Lifecycle Simulation</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #050507;
            color: #e2e8f0;
            overflow-x: hidden;
        }
        /* Custom range slider styling */
        input[type=range] {
            accent-color: #a855f7;
        }
        canvas {
            image-rendering: pixelated;
        }
    </style>
</head>
<body class="h-screen w-screen flex flex-col items-center justify-between p-2 md:p-6 select-none bg-radial from-slate-900 via-black to-black">

    <!-- Top Navigation Header -->
    <header class="w-full max-w-5xl flex justify-between items-center z-10 py-2 px-4 rounded-xl bg-slate-900/60 backdrop-blur-md border border-slate-800">
        <div class="flex items-center space-x-3">
            <div class="w-3 h-3 rounded-full bg-purple-500 animate-pulse"></div>
            <h1 class="text-lg md:text-xl font-semibold tracking-wide bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-pink-400 to-amber-300">
                Pointillism Flower Simulation
            </h1>
        </div>
        <div class="text-xs text-slate-400 hidden sm:block">
            Lifecycle Time: <span id="time-display" class="font-mono text-purple-300 font-bold">0.00</span>s / 45.0s
        </div>
    </header>

    <!-- Canvas Container -->
    <main class="relative flex-1 w-full max-w-5xl my-2 flex items-center justify-center overflow-hidden rounded-2xl bg-black border border-slate-800/80 shadow-2xl shadow-purple-950/20">
        <canvas id="flowerCanvas" class="max-w-full max-h-full object-contain cursor-pointer"></canvas>

        <!-- Overlay Status Badge -->
        <div id="status-badge" class="absolute top-4 left-4 px-3 py-1 text-xs rounded-full bg-slate-900/80 border border-slate-700/50 backdrop-blur text-purple-300 pointer-events-none transition-opacity duration-300 opacity-0">
            Paused
        </div>
    </main>

    <!-- Bottom Controls Deck -->
    <footer class="w-full max-w-5xl z-10 flex flex-col gap-3 p-4 rounded-xl bg-slate-900/70 backdrop-blur-md border border-slate-800">
        <!-- Timeline Slider -->
        <div class="flex items-center space-x-3 w-full">
            <span class="text-xs font-mono text-slate-400 w-10 text-right" id="slider-time">0.0s</span>
            <input id="timeline" type="range" min="0" max="45" step="0.05" value="0" class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer">
            <span class="text-xs font-mono text-slate-400 w-10">45.0s</span>
        </div>

        <!-- Buttons and Speed Control -->
        <div class="flex flex-wrap justify-between items-center gap-3">
            <div class="flex items-center space-x-2">
                <!-- Play/Pause Button -->
                <button id="btn-play" class="flex items-center justify-center px-4 py-2 text-sm font-medium rounded-lg bg-purple-600 hover:bg-purple-500 active:scale-95 transition text-white shadow-lg shadow-purple-600/30">
                    <svg id="icon-play" class="w-4 h-4 mr-1.5 fill-current" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                    <svg id="icon-pause" class="w-4 h-4 mr-1.5 fill-current hidden" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
                    <span id="label-play">Play</span>
                </button>

                <!-- Restart Button -->
                <button id="btn-restart" class="flex items-center justify-center px-3 py-2 text-sm font-medium rounded-lg bg-slate-800 hover:bg-slate-700 active:scale-95 transition text-slate-200">
                    <svg class="w-4 h-4 mr-1 fill-current" viewBox="0 0 24 24"><path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/></svg>
                    Restart
                </button>

                <!-- Loop Toggle -->
                <button id="btn-loop" class="px-3 py-2 text-sm font-medium rounded-lg bg-slate-800 border border-slate-700 hover:bg-slate-700 active:scale-95 transition text-slate-400">
                    Loop: OFF
                </button>
            </div>

            <!-- Speed Selector -->
            <div class="flex items-center space-x-2 text-xs text-slate-300">
                <label for="speed-select" class="font-medium text-slate-400">Speed:</label>
                <select id="speed-select" class="bg-slate-800 border border-slate-700 text-slate-200 rounded-lg px-2.5 py-1.5 focus:ring-1 focus:ring-purple-500 outline-none">
                    <option value="0.5">0.5x</option>
                    <option value="1.0" selected>1.0x</option>
                    <option value="1.5">1.5x</option>
                    <option value="2.0">2.0x</option>
                </select>
            </div>

            <!-- Keyboard Hints -->
            <div class="hidden lg:flex items-center space-x-3 text-xs text-slate-500">
                <span><kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">Space</kbd> Toggle Play</span>
                <span><kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">R</kbd> Restart</span>
            </div>
        </div>
    </footer>

    <!-- Main Logic Ported from Python Script -->
    <script>
        // Seeded Pseudo-Random Generator (Linear Congruential Generator / Mulberry32)
        class SeededRNG {
            constructor(seed = 5) {
                this.seed = seed;
            }
            random() {
                let t = this.seed += 0x6D2B79F5;
                t = Math.imul(t ^ (t >>> 15), t | 1);
                t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
                return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
            }
            uniform(min, max) {
                return min + (max - min) * this.random();
            }
            normal(mean = 0, std = 1) {
                // Box-Muller transform
                let u1 = this.random();
                let u2 = this.random();
                while (u1 <= 1e-15) u1 = this.random();
                let z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
                return mean + z0 * std;
            }
            choice(arr, p = null) {
                if (!p) return arr[Math.floor(this.random() * arr.length)];
                let r = this.random(), cumulative = 0;
                for (let i = 0; i < arr.length; i++) {
                    cumulative += p[i];
                    if (r <= cumulative) return arr[i];
                }
                return arr[arr.length - 1];
            }
            permutation(n) {
                let arr = Array.from({length: n}, (_, i) => i);
                for (let i = n - 1; i > 0; i--) {
                    let j = Math.floor(this.random() * (i + 1));
                    [arr[i], arr[j]] = [arr[j], arr[i]];
                }
                return arr;
            }
            integers(min, max, count) {
                let out = [];
                for (let i = 0; i < count; i++) {
                    out.push(Math.floor(this.uniform(min, max)));
                }
                return out;
            }
        }

        // Keyframes for state interpolation [t, stem, size, bloom, wilt, leaf, glow]
        const KEYS = [
            [0.0, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00],
            [5.0, 0.42, 0.22, 0.00, 0.0, 0.25, 0.00],
            [10.0, 0.62, 0.42, 0.00, 0.0, 0.50, 0.35],
            [16.0, 0.80, 0.68, 0.50, 0.0, 0.72, 0.55],
            [24.0, 1.00, 1.00, 1.00, 0.0, 1.00, 1.00],
            [30.0, 1.00, 1.00, 1.00, 0.0, 1.00, 1.00],
            [39.0, 0.98, 0.85, 0.55, 1.0, 0.92, 0.00],
            [45.0, 0.98, 0.85, 0.55, 1.0, 0.90, 0.00]
        ];
        const T_END = KEYS[KEYS.length - 1][0];

        // Palettes
        const SOIL_PAL = [[34, 25, 20], [50, 36, 28], [68, 50, 37], [88, 65, 47], [108, 82, 60], [64, 58, 52]];
        const STEM_PAL = [[62, 38, 120], [100, 58, 165], [140, 84, 200], [60, 160, 140]];
        const STEM_WILT = [[120, 88, 66], [96, 66, 52], [140, 108, 76]];
        const LEAF_PAL = [[60, 150, 140], [80, 120, 175], [130, 80, 195], [175, 105, 215]];
        const LEAF_WILT = [[130, 100, 70], [104, 76, 58], [146, 116, 84]];
        const RIB_PAL = [[210, 180, 255], [170, 230, 220]];
        const WILT_PAL = [[150, 86, 128], [116, 64, 108], [88, 52, 88], [126, 94, 104], [104, 72, 56]];
        const RIM_PAL = [[205, 165, 255], [255, 190, 250], [170, 140, 255]];
        const HI_PAL = [[235, 215, 255], [255, 225, 250]];
        const GOLD_PAL = [[255, 214, 110], [255, 238, 170], [255, 184, 90]];
        const STAMEN_PAL = [[255, 240, 255], [255, 215, 235], [255, 230, 150], [255, 190, 80]];
        const STAMEN_WILT = [[140, 112, 84], [120, 96, 72]];

        const LAYERS = [
            {n:8, ac:0.60, ao:1.00, kc:-1.20, ko:0.45, L:1.00, wc:0.20, wo:0.34, d:1150, off:0.00, pal:[[210, 80, 225], [170, 58, 225], [128, 50, 218], [96, 44, 205], [78, 42, 185]]},
            {n:6, ac:0.48, ao:0.68, kc:-1.05, ko:0.15, L:0.88, wc:0.19, wo:0.31, d:950, off:0.40, pal:[[255, 150, 235], [245, 92, 218], [205, 62, 218], [150, 52, 222]]},
            {n:5, ac:0.36, ao:0.46, kc:-0.85, ko:-0.05, L:0.72, wc:0.17, wo:0.27, d:760, off:0.20, pal:[[255, 205, 245], [255, 135, 232], [238, 84, 216], [195, 62, 226]]},
            {n:4, ac:0.22, ao:0.32, kc:-0.50, ko:-0.10, L:0.46, wc:0.14, wo:0.22, d:480, off:0.55, pal:[[255, 238, 252], [255, 185, 242], [255, 125, 228]]}
        ];

        const LEAF_DEFS = [
            [0.10, +1, 1.00, 0.55, -0.80],
            [0.16, -1, 0.90, 0.50, -0.85],
            [0.40, +1, 0.70, 0.95, -0.70],
            [0.33, -1, 0.62, 0.90, -0.65]
        ];

        // Offsets table for drawing circular particle splats
        const _OFF = [];
        for (let dy = -3; dy <= 3; dy++) {
            for (let dx = -3; dx <= 3; dx++) {
                if (dx * dx + dy * dy <= 9) {
                    _OFF.push([dx, dy]);
                }
            }
        }
        _OFF.sort((a, b) => (a[0]*a[0] + a[1]*a[1]) - (b[0]*b[0] + b[1]*b[1]));

        // Helper Math functions
        function smoothstep(x, a, b) {
            let t = Math.min(Math.max((x - a) / (b - a), 0), 1);
            return t * t * (3 - 2 * t);
        }

        function sinc(x) {
            if (Math.abs(x) < 1e-6) return 1.0;
            let px = x * Math.PI;
            return Math.sin(px) / px;
        }

        function profile(u) {
            let clamped = Math.min(Math.max(u, 0), 1);
            return Math.pow(Math.sin(Math.PI * Math.pow(clamped, 0.75)), 0.85);
        }

        function palettePick(rng, pal, gVal, spread = 0.55, jitter = 0.07) {
            let x = Math.min(Math.max(gVal, 0), 1) * (pal.length - 1) + rng.normal(0, spread);
            let idx = Math.min(Math.max(Math.round(x), 0), pal.length - 1);
            let base = pal[idx];
            let factor = 1 + rng.normal(0, jitter);
            return [base[0] * factor, base[1] * factor, base[2] * factor];
        }

        function areaU(rng, n) {
            let out = [];
            while (out.length < n) {
                let u = rng.random();
                if (rng.random() < profile(u)) {
                    out.push(u);
                }
            }
            return out;
        }

        function sampleV(rng, n, rim = 0.14) {
            let v = [];
            for (let i = 0; i < n; i++) {
                let val = rng.uniform(-1, 1);
                if (rng.random() < rim) {
                    val = Math.sign(val || 1) * rng.uniform(0.88, 1.0);
                }
                v.push(val);
            }
            return v;
        }

        function getState(t) {
            t = Math.min(Math.max(t, 0.0), T_END);
            let ts = KEYS.map(k => k[0]);
            let idx = 0;
            while (idx < ts.length - 2 && ts[idx + 1] <= t) idx++;
            
            let u = (t - ts[idx]) / (ts[idx + 1] - ts[idx]);
            let p0 = KEYS[Math.max(idx - 1, 0)].slice(1);
            let p1 = KEYS[idx].slice(1);
            let p2 = KEYS[idx + 1].slice(1);
            let p3 = KEYS[Math.min(idx + 2, KEYS.length - 1)].slice(1);

            let res = [];
            for (let k = 0; k < 6; k++) {
                let v = 0.5 * (2 * p1[k] + (p2[k] - p0[k]) * u + 
                    (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u * u + 
                    (3 * p1[k] - p0[k] - 3 * p2[k] + p3[k]) * u * u * u);
                res.push(Math.min(Math.max(v, 0), 1));
            }
            return res; // [stem, size, bloom, wilt, leaf, glow]
        }

        function bez(P, s) {
            let [P0, P1, P2, P3] = P;
            let q = 1 - s;
            let x = q*q*q * P0[0] + 3*q*q*s * P1[0] + 3*q*s*s * P2[0] + s*s*s * P3[0];
            let y = q*q*q * P0[1] + 3*q*q*s * P1[1] + 3*q*s*s * P2[1] + s*s*s * P3[1];
            let dx = 3*q*q * (P1[0] - P0[0]) + 6*q*s * (P2[0] - P1[0]) + 3*s*s * (P3[0] - P2[0]);
            let dy = 3*q*q * (P1[1] - P0[1]) + 6*q*s * (P2[1] - P1[1]) + 3*s*s * (P3[1] - P2[1]);
            return [x, y, dx, dy];
        }

        function mixcol(live, wilt, w) {
            return [
                live[0] + (wilt[0] - live[0]) * w,
                live[1] + (wilt[1] - live[1]) * w,
                live[2] + (wilt[2] - live[2]) * w
            ];
        }

        // Particle Splatting onto Canvas Pixel Buffer
        function splat(pixels, width, height, x, y, r, g, b, rad, nmax = 13) {
            let xi = Math.round(x);
            let yi = Math.round(y);
            let radSq = rad * rad + 0.01;
            r = Math.min(Math.max(Math.round(r), 0), 255);
            g = Math.min(Math.max(Math.round(g), 0), 255);
            b = Math.min(Math.max(Math.round(b), 0), 255);

            for (let i = 0; i < nmax && i < _OFF.length; i++) {
                let dx = _OFF[i][0];
                let dy = _OFF[i][1];
                if (dx * dx + dy * dy <= radSq) {
                    let px = xi + dx;
                    let py = yi + dy;
                    if (px >= 0 && px < width && py >= 0 && py < height) {
                        let idx = (py * width + px) * 4;
                        pixels[idx] = r;
                        pixels[idx + 1] = g;
                        pixels[idx + 2] = b;
                        pixels[idx + 3] = 255;
                    }
                }
            }
        }

        // Particle Batch Collector
        class Batch {
            constructor() {
                this.items = [];
            }
            add(x, y, col, rad, z) {
                this.items.push({x, y, col, rad, z});
            }
            draw(pixels, width, height) {
                if (!this.items.length) return;
                // Sort by z-order
                this.items.sort((a, b) => a.z - b.z);
                for (let i = 0; i < this.items.length; i++) {
                    let item = this.items[i];
                    splat(pixels, width, height, item.x, item.y, item.col[0], item.col[1], item.col[2], item.rad);
                }
            }
        }

        // Main Plant Lifecycle Builder & Renderer
        class Plant {
            constructor(W, H) {
                this.W = W;
                this.H = H;
                this.rng = new SeededRNG(5);
                this.cx = W / 2;
                this.y0 = H * 0.80;
                this.Ls = H * 0.38;
                this.Lf = H * 0.235;

                this.buildSoil();
                this.buildStem();
                this.buildHead();
                this.buildStamens();
                this.buildLeaves();
                this.buildFx();
            }

            surface(x) {
                let H = this.H;
                return (this.y0 - 0.022 * H * Math.exp(-Math.pow((x - this.cx) / (0.2 * this.W), 2))
                        - 0.003 * H * Math.sin(x * 0.045) - 0.002 * H * Math.sin(x * 0.13 + 1.3));
            }

            buildSoil() {
                let { W, H, rng } = this;
                this.soilParticles = [];
                let n = 22000;
                for (let i = 0; i < n; i++) {
                    let x = rng.uniform(0, W);
                    let d = Math.pow(rng.random(), 1.5) * 0.14 * H;
                    let y = this.surface(x) + d;
                    let depth = d / (0.14 * H);
                    let edge = Math.pow(Math.min(Math.max(Math.min(x, W - x) / (0.2 * W), 0), 1), 0.8);
                    let clump = 0.5 + 0.5 * Math.sin(x * 0.07 + y * 0.05) * Math.sin(y * 0.11 - x * 0.03);
                    let bright = Math.pow(1 - depth, 0.8) * edge * (0.55 + 0.35 * clump + 0.35 * rng.random());
                    let col = palettePick(rng, SOIL_PAL, rng.random(), 1.0);
                    col = col.map(c => c * bright);
                    let rad = rng.choice([1.0, 1.5, 2.0], [0.4, 0.4, 0.2]);
                    this.soilParticles.push({x, y, col, rad, nmax: 13});
                }

                // Rocks/Pebbles
                let k = 170;
                for (let i = 0; i < k; i++) {
                    let px = rng.uniform(0.05 * W, 0.95 * W);
                    let py = this.surface(px) + Math.pow(rng.random(), 1.3) * 0.1 * H;
                    let pc = palettePick(rng, [[58, 52, 48], [84, 74, 64], [104, 90, 76], [46, 38, 32]], rng.random(), 0.7);
                    let edge = Math.pow(Math.min(Math.max(Math.min(px, W - px) / (0.2 * W), 0), 1), 0.8);
                    pc = pc.map(c => c * edge);
                    let rad = rng.choice([2.0, 3.0], [0.6, 0.4]);
                    this.soilParticles.push({x: px, y: py, col: pc, rad, nmax: 29});
                }

                // Soil Crumbs (Animated dynamic particles)
                let m = 520;
                this.cr = [];
                for (let i = 0; i < m; i++) {
                    let cx = this.cx + rng.normal(0, 0.03 * H);
                    this.cr.push({
                        x: cx,
                        y: this.surface(cx) - rng.random() * 0.006 * H,
                        amp: H * 0.05 * Math.pow(rng.random(), 2.2),
                        delay: rng.uniform(0, 2.5),
                        col: palettePick(rng, SOIL_PAL, rng.uniform(0.3, 1), 0.8).map(c => c * 0.8),
                        rad: rng.choice([1.0, 1.5, 2.0], [0.4, 0.4, 0.2])
                    });
                }
            }

            buildStem() {
                let { rng } = this;
                let n = 3600;
                this.stemData = [];
                for (let i = 0; i < n; i++) {
                    let s = rng.random();
                    let lat = rng.uniform(-1, 1);
                    if (rng.random() < 0.18) {
                        lat = Math.sign(lat || 1) * rng.uniform(0.85, 1.0);
                    }
                    let live = palettePick(rng, STEM_PAL.slice(0, 3), s * 0.8 + rng.random() * 0.2);
                    if (rng.random() < 0.12) {
                        let factor = 1 + rng.normal(0, 0.08);
                        live = STEM_PAL[3].map(c => c * factor);
                    }
                    let wilt = palettePick(rng, STEM_WILT, rng.random(), 0.8);
                    let rad = rng.choice([1.0, 1.5, 2.0], [0.35, 0.45, 0.2]);
                    this.stemData.push({ s, lat, live, wilt, rn: rng.random(), rad });
                }
                // Permute
                this.stemData = rng.permutation(n).map(i => this.stemData[i]);
            }

            ctrl(L, wilt, sway) {
                let cx = this.cx, y0 = this.y0;
                let P0 = [cx, y0 + 4.0];
                let P1 = [cx - 0.06 * L * (1 - wilt) + 0.02 * L * wilt, y0 - 0.33 * L];
                let P2 = [cx + 0.05 * L * (1 - wilt) + 0.08 * L * wilt + sway * 0.5, y0 - L * (0.74 + 0.30 * wilt)];
                let P3 = [cx + sway + 0.32 * L * wilt, y0 - L * (1 - 0.15 * wilt)];
                return [P0, P1, P2, P3];
            }

            buildHead() {
                let { rng } = this;
                this.headData = [];
                for (let Ly of LAYERS) {
                    let d = Ly.d;
                    for (let i = 0; i < Ly.n; i++) {
                        let th = 2 * Math.PI * i / Ly.n + Ly.off + rng.normal(0, 0.10);
                        let aj = rng.normal(0, 0.06);
                        let lj = rng.uniform(0.92, 1.08);
                        let pj = rng.random();
                        let wj = rng.uniform(-0.5, 0.5);
                        let uArr = areaU(rng, d);
                        let vArr = sampleV(rng, d);

                        for (let k = 0; k < d; k++) {
                            let u = uArr[k], v = vArr[k];
                            let col = palettePick(rng, Ly.pal, u + rng.normal(0, 0.10));
                            if (Math.abs(v) > 0.86 && rng.random() < 0.55) {
                                col = palettePick(rng, RIM_PAL, rng.random());
                            }
                            if (rng.random() < 0.04) {
                                col = palettePick(rng, HI_PAL, rng.random());
                            }
                            if (rng.random() < 0.02 && u < 0.55) {
                                col = palettePick(rng, GOLD_PAL, rng.random());
                            }
                            let wilt = palettePick(rng, WILT_PAL, 0.4 * u + 0.6 * rng.random(), 0.7);
                            let rad = rng.choice([1.0, 1.5, 2.0], [0.3, 0.45, 0.25]);

                            this.headData.push({
                                th, aj, pj, wj, u, v,
                                ac: Ly.ac, ao: Ly.ao, kc: Ly.kc, ko: Ly.ko,
                                L: Ly.L * lj, wc: Ly.wc, wo: Ly.wo,
                                live: col, wilt: wilt, rn: rng.random(), rad,
                                sp: profile(u)
                            });
                        }
                    }
                }
                this.headData = rng.permutation(this.headData.length).map(i => this.headData[i]);
            }

            buildStamens() {
                let { rng } = this;
                let n = 700, nf = 60;
                let fTh = Array.from({length: nf}, () => rng.uniform(0, 2 * Math.PI));
                let fBeta = Array.from({length: nf}, () => rng.uniform(0.2, 0.85));
                let fEll = Array.from({length: nf}, () => rng.uniform(0.30, 0.55));

                this.stamenData = [];
                for (let i = 0; i < n; i++) {
                    let fid = Math.floor(rng.uniform(0, nf));
                    let t = 1 - Math.pow(rng.random(), 1.6);
                    let live = palettePick(rng, STAMEN_PAL, t, 0.35);
                    let wilt = palettePick(rng, STAMEN_WILT, rng.random(), 0.6);
                    let rad = (t > 0.88) ? 2.0 : rng.choice([1.0, 1.5]);
                    this.stamenData.push({
                        th: fTh[fid], beta: fBeta[fid], ell: fEll[fid], t, live, wilt, rad
                    });
                }
                this.stamenData = rng.permutation(n).map(i => this.stamenData[i]);
            }

            buildLeaves() {
                let { rng } = this;
                this.leafData = [];
                let d = 900;
                for (let j = 0; j < LEAF_DEFS.length; j++) {
                    let uArr = areaU(rng, d);
                    let vArr = sampleV(rng, d, 0.10);
                    for (let k = 0; k < d; k++) {
                        let u = uArr[k], v = vArr[k];
                        let isRib = rng.random() < 0.09;
                        if (isRib) v = rng.normal(0, 0.03);
                        let live = palettePick(rng, LEAF_PAL, u + rng.normal(0, 0.1));
                        if (isRib) live = palettePick(rng, RIB_PAL, rng.random());
                        let wilt = palettePick(rng, LEAF_WILT, rng.random(), 0.8);
                        let rad = rng.choice([1.0, 1.5, 2.0], [0.35, 0.45, 0.2]);

                        this.leafData.push({
                            lid: j, u, v, live, wilt, rn: rng.random(), rad
                        });
                    }
                }
                this.leafData = rng.permutation(this.leafData.length).map(i => this.leafData[i]);
            }

            buildFx() {
                let { rng, H } = this;
                let n = 1800;
                this.halo = [];
                for (let i = 0; i < n; i++) {
                    let r = Math.min(Math.abs(rng.normal(0, 0.55)), 1.6);
                    this.halo.push({
                        a: rng.uniform(0, 2 * Math.PI), r,
                        b: Math.pow(1 - r / 1.6, 1.5) * 0.55,
                        fl: rng.random()
                    });
                }
                this.halo = rng.permutation(n).map(i => this.halo[i]);

                this.ring = [];
                for (let j = 0; j < 7; j++) {
                    let m = (j === 0) ? 700 : 170;
                    for (let k = 0; k < m; k++) {
                        this.ring.push({
                            cf: (j === 0) ? 0.0 : 0.5,
                            cj: Math.max(j - 1, 0),
                            rho: (j === 0) ? 1.0 : 0.5,
                            a: rng.uniform(0, 2 * Math.PI),
                            fl: rng.random()
                        });
                    }
                }
                this.ring = rng.permutation(this.ring.length).map(i => this.ring[i]);

                let mSp = 280;
                this.spark = [];
                for (let i = 0; i < mSp; i++) {
                    this.spark.push({
                        a: rng.uniform(0, 2 * Math.PI),
                        rho: rng.random(),
                        ph: rng.random(),
                        sp: rng.uniform(0.6, 1.4),
                        rad: rng.choice([1.0, 2.0], [0.7, 0.3]),
                        hue: rng.random()
                    });
                }

                let mFall = 260;
                this.fall = [];
                for (let i = 0; i < mFall; i++) {
                    let xl = this.cx + rng.normal(0, 0.12 * H);
                    this.fall.push({
                        r0: rng.random(),
                        ox: rng.normal(0, 1),
                        oy: rng.normal(0, 1),
                        xl, yl: this.surface(xl) - rng.random() * 0.012 * H,
                        ph: rng.uniform(0, 6.28),
                        col: palettePick(rng, WILT_PAL, rng.random(), 0.8),
                        rad: rng.choice([1.5, 2.0])
                    });
                }
            }

            render(t, ctx, pixelBuffer) {
                let H = this.H, W = this.W;
                let [stem, size, bloom, wilt, leaf, glow] = getState(t);
                
                // Clear buffer with base soil
                let pixels = pixelBuffer.data;
                pixels.fill(0); // clear to transparent black

                // Draw pre-calculated base soil
                for (let i = 0; i < this.soilParticles.length; i++) {
                    let p = this.soilParticles[i];
                    splat(pixels, W, H, p.x, p.y, p.col[0], p.col[1], p.col[2], p.rad, p.nmax);
                }

                let B = new Batch();
                let nodes = new Batch();
                let Lf = this.Lf;

                let L = this.Ls * stem;
                let sway = 0.012 * H * Math.sin(t * 0.9) * stem * (1 - 0.6 * wilt);
                let P = this.ctrl(L, wilt, sway);
                let [hx, hy] = P[3];

                // Render Stem
                if (stem > 0.01) {
                    let nv = Math.floor(this.stemData.length * Math.min(Math.max(stem, 0.08), 1));
                    for (let i = 0; i < nv; i++) {
                        let item = this.stemData[i];
                        let [x, y, dx, dy] = bez(P, item.s);
                        let nn = Math.hypot(dx, dy) + 1e-6;
                        let wst = 0.0085 * H * (1 - 0.3 * item.s) * (1 - 0.25 * wilt) * Math.min(Math.max(0.4 + stem * 1.2, 0.4), 1);
                        let lat = item.lat * wst;
                        let wi = Math.min(Math.max(wilt * (0.75 + 0.5 * item.s) * (0.7 + 0.5 * item.rn), 0), 1);
                        let col = mixcol(item.live, item.wilt, wi);
                        B.add(x - dy / nn * lat, y + dx / nn * lat, col, item.rad, -500.0);
                    }
                }

                // Render Leaves
                if (leaf > 0.02 && stem > 0.05) {
                    let nv = Math.floor(this.leafData.length * Math.min(Math.max(leaf, 0.15), 1));
                    let sa = LEAF_DEFS.map(d => d[0]);
                    let aPos = sa.map(s => bez(P, s));

                    for (let i = 0; i < nv; i++) {
                        let item = this.leafData[i];
                        let lid = item.lid;
                        let dDef = LEAF_DEFS[lid];
                        let [ax, ay] = [aPos[lid][0], aPos[lid][1]];
                        let m = dDef[1];
                        let lfac = dDef[2];
                        let a0 = dDef[3] + (1 - leaf) * 0.8 - 0.6 * wilt;
                        let c = dDef[4] - 0.5 * wilt;
                        let u = item.u, v = item.v;
                        let LL = 0.19 * H * lfac * leaf * (1 - 0.25 * wilt);
                        let am = a0 + c * u * 0.5;
                        let al = a0 + c * u;
                        let sc = sinc(c * u * 0.5);
                        let lat = v * 0.27 * LL * profile(u);
                        let X = ax + LL * u * m * Math.cos(am) * sc - lat * Math.sin(al);
                        let Yup = LL * u * Math.sin(am) * sc + lat * m * Math.cos(al);
                        let wi = Math.min(Math.max(wilt * (0.9 + 0.5 * u + 0.3 * item.rn) - 0.1, 0), 1);
                        let col = mixcol(item.live, item.wilt, wi);
                        B.add(X, ay - Yup, col, item.rad, -450.0);
                    }
                }

                // Render Flower Head & Petals
                if (stem > 0.01 && size > 0.05) {
                    let phi = wilt * 2.75 + 0.035 * Math.sin(t * 0.9 + 1.0) * (1 - wilt);
                    let tau = 0.20 + 0.36 * bloom - 0.40 * wilt;
                    let cphi = Math.cos(phi), sphi = Math.sin(phi);
                    let ct = Math.cos(tau), st_ = Math.sin(tau);
                    let Ls_ = Lf * size;

                    let project = (xl, yl, zl) => {
                        let yp = yl * ct - zl * st_;
                        let zp = yl * st_ + zl * ct;
                        return [hx + xl * cphi + yp * sphi, hy - (-xl * sphi + yp * cphi), zp, yp];
                    };

                    let vis = Math.min(Math.max(size * size * 1.15, 0.2), 1.0);
                    let nv = Math.floor(this.headData.length * vis);

                    for (let i = 0; i < nv; i++) {
                        let g = this.headData[i];
                        let u = g.u, v = g.v;
                        let A0 = g.ac + (g.ao - g.ac) * bloom + g.aj;
                        A0 = A0 * (1 - 0.55 * wilt) + wilt * g.wj * 0.3;
                        let K = g.kc + (g.ko - g.kc) * bloom + wilt * (0.6 + 0.6 * g.pj);
                        let Lp = Ls_ * g.L * (1 - 0.28 * wilt * g.pj);
                        let am = A0 + K * u * 0.5;
                        let sc = sinc(K * u * 0.5);
                        let rr = Lp * u * Math.sin(am) * sc;
                        let hh = Lp * u * Math.cos(am) * sc;
                        let lat = v * (g.wc + (g.wo - g.wc) * bloom) * Lp * g.sp;
                        rr = rr + 0.025 * Ls_ - 0.5 * lat * lat / (Lp + 1.0);
                        let cth = Math.cos(g.th), sth = Math.sin(g.th);
                        
                        let [X, Y, zp, yp] = project(cth * rr - sth * lat, hh, sth * rr + cth * lat);
                        let shade = Math.min(Math.max(0.72 + 0.28 * Math.min(Math.max(zp / Ls_ * 0.5 + 0.5, 0), 1) + 0.12 * (hh / Ls_), 0.5), 1.2);
                        let wi = Math.min(Math.max(wilt * (1.0 + 0.7 * u + 0.4 * g.rn) - 0.2, 0), 1);
                        let col = mixcol(g.live, g.wilt, wi).map(c => c * shade);
                        B.add(X, Y, col, g.rad, zp);
                    }

                    // Stamens
                    let ss = smoothstep(bloom, 0.30, 0.85);
                    if (ss > 0.02) {
                        let nv2 = Math.floor(this.stamenData.length * Math.min(Math.max(size * size, 0.25), 1));
                        for (let i = 0; i < nv2; i++) {
                            let S = this.stamenData[i];
                            let ell = Ls_ * ss * S.ell;
                            let beta = S.beta * (0.6 + 0.4 * bloom) + wilt * 0.3;
                            let r = ell * S.t * Math.sin(beta) + 0.02 * Ls_;
                            let yl = 0.05 * Ls_ + ell * S.t * Math.cos(beta);
                            let [X, Y, zp] = project(Math.cos(S.th) * r, yl, Math.sin(S.th) * r);
                            let col = mixcol(S.live, S.wilt, wilt);
                            B.add(X, Y, col, S.rad, zp + 3.0);
                        }
                    }

                    // Glow & Energy Ring Effects
                    if (glow > 0.02) {
                        let axis = [Math.sin(phi), -Math.cos(phi)];
                        let ccx = hx + axis[0] * 0.5 * Ls_;
                        let ccy = hy + axis[1] * 0.5 * Ls_;

                        let nh = Math.floor(this.halo.length * glow);
                        for (let i = 0; i < nh; i++) {
                            let Hh = this.halo[i];
                            let rh = Hh.r * Ls_ * 1.1;
                            let br = Hh.b * glow * (0.85 + 0.3 * Math.sin(t * 1.3 + Hh.fl * 6.28));
                            B.add(ccx + Math.cos(Hh.a) * rh, ccy + Math.sin(Hh.a) * rh,
                                  [150 * br, 70 * br, 240 * br], 1.0, -2000.0);
                        }

                        let nr = Math.floor(this.ring.length * glow);
                        let Rs = Ls_ * 1.25;
                        for (let i = 0; i < nr; i++) {
                            let R = this.ring[i];
                            let cang = 2 * Math.PI * R.cj / 6 + t * 0.15;
                            let a = R.a + t * 0.05;
                            let rx = ccx + Rs * (R.cf * Math.cos(cang) + R.rho * Math.cos(a));
                            let ry = ccy + Rs * (R.cf * Math.sin(cang) + R.rho * Math.sin(a));
                            let bb = (0.40 + 0.60 * glow) * (0.65 + 0.35 * Math.sin(t * 2 + R.fl * 20));
                            B.add(rx, ry, [210 * bb, 145 * bb, 255 * bb], 1.0, -1500.0);
                        }

                        for (let j = 0; j < 6; j++) {
                            let ja = 2 * Math.PI * j / 6 + t * 0.15;
                            nodes.add(ccx + Rs * Math.cos(ja), ccy + Rs * Math.sin(ja),
                                      [255 * glow, 215 * glow, 255 * glow], 3.0, 0.0);
                        }

                        let mSp = this.spark.length;
                        for (let i = 0; i < mSp; i++) {
                            let Sp = this.spark[i];
                            let life = (t * 0.10 * Sp.sp + Sp.ph) % 1.0;
                            let rho = (0.25 + 1.15 * Sp.rho) * Ls_ * (0.6 + 0.6 * life);
                            let px = ccx + Math.cos(Sp.a) * rho;
                            let py = ccy + Math.sin(Sp.a) * rho - life * 0.25 * Ls_;
                            let bs = Math.pow(Math.sin(Math.PI * life), 0.8) * glow;
                            let baseCol = (Sp.hue < 0.5) ? [255, 215, 255] : [255, 150, 235];
                            B.add(px, py, baseCol.map(c => c * bs), Sp.rad, 2000.0);
                        }
                    }

                    // Falling Petal Particles during Wilting
                    if (wilt > 0.02) {
                        for (let i = 0; i < this.fall.length; i++) {
                            let F = this.fall[i];
                            let fp = Math.min(Math.max((wilt * 1.05 - F.r0 * 0.7) / 0.35, 0), 1);
                            if (fp > 0) {
                                let sx = hx + F.ox * 0.18 * Ls_;
                                let sy = hy + F.oy * 0.18 * Ls_ + 0.25 * Ls_;
                                let x = sx + (F.xl - sx) * fp + Math.sin(fp * 6.28 + F.ph) * 0.03 * H * (1 - fp);
                                let y = sy + (F.yl - sy) * fp * fp;
                                B.add(x, y, F.col, F.rad, 500.0);
                            }
                        }
                    }
                }

                // Draw batched dynamic particles
                B.draw(pixels, W, H);
                if (nodes.items.length) {
                    for (let item of nodes.items) {
                        splat(pixels, W, H, item.x, item.y, item.col[0], item.col[1], item.col[2], item.rad, 29);
                    }
                }

                // Animated Soil Crumbs
                for (let i = 0; i < this.cr.length; i++) {
                    let C = this.cr[i];
                    let e = Math.min(Math.max((t - C.delay) / 3.0, 0), 1);
                    let sy = C.y - C.amp * Math.sin(Math.PI * e);
                    splat(pixels, W, H, C.x, sy, C.col[0], C.col[1], C.col[2], C.rad, 13);
                }

                // Put image data back to Canvas Context
                ctx.putImageData(pixelBuffer, 0, 0);
            }
        }

        // Web Application Controller Setup
        window.onload = function() {
            const canvas = document.getElementById('flowerCanvas');
            const ctx = canvas.getContext('2d');
            const timeline = document.getElementById('timeline');
            const timeDisplay = document.getElementById('time-display');
            const sliderTime = document.getElementById('slider-time');
            const btnPlay = document.getElementById('btn-play');
            const btnRestart = document.getElementById('btn-restart');
            const btnLoop = document.getElementById('btn-loop');
            const speedSelect = document.getElementById('speed-select');
            const iconPlay = document.getElementById('icon-play');
            const iconPause = document.getElementById('icon-pause');
            const labelPlay = document.getElementById('label-play');
            const statusBadge = document.getElementById('status-badge');

            // Fixed internal resolution matching aspect ratio
            const SIZE = 640;
            canvas.width = SIZE;
            canvas.height = SIZE;

            let pixelBuffer = ctx.createImageData(SIZE, SIZE);
            let plant = new Plant(SIZE, SIZE);

            let currentTime = 0.0;
            let isPlaying = true;
            let isLooping = false;
            let timeScale = 1.0;
            let lastTimestamp = performance.now();

            function updateUI() {
                timeline.value = currentTime.toFixed(2);
                timeDisplay.textContent = currentTime.toFixed(2);
                sliderTime.textContent = currentTime.toFixed(1) + 's';

                if (isPlaying) {
                    iconPlay.classList.add('hidden');
                    iconPause.classList.remove('hidden');
                    labelPlay.textContent = 'Pause';
                    statusBadge.style.opacity = '0';
                } else {
                    iconPlay.classList.remove('hidden');
                    iconPause.classList.add('hidden');
                    labelPlay.textContent = 'Play';
                    statusBadge.style.opacity = '1';
                }

                if (isLooping) {
                    btnLoop.classList.remove('text-slate-400', 'border-slate-700');
                    btnLoop.classList.add('text-purple-400', 'border-purple-500', 'bg-purple-950/30');
                    btnLoop.textContent = 'Loop: ON';
                } else {
                    btnLoop.classList.add('text-slate-400', 'border-slate-700');
                    btnLoop.classList.remove('text-purple-400', 'border-purple-500', 'bg-purple-950/30');
                    btnLoop.textContent = 'Loop: OFF';
                }
            }

            function animate(now) {
                let dt = (now - lastTimestamp) / 1000.0;
                lastTimestamp = now;

                if (isPlaying) {
                    currentTime += dt * timeScale;
                    if (currentTime > T_END) {
                        if (isLooping) {
                            currentTime = 0.0;
                        } else {
                            currentTime = T_END;
                            isPlaying = false;
                        }
                    }
                    updateUI();
                }

                plant.render(currentTime, ctx, pixelBuffer);
                requestAnimationFrame(animate);
            }

            // Event Listeners
            btnPlay.addEventListener('click', () => {
                if (currentTime >= T_END) currentTime = 0.0;
                isPlaying = !isPlaying;
                updateUI();
            });

            btnRestart.addEventListener('click', () => {
                currentTime = 0.0;
                isPlaying = true;
                updateUI();
            });

            btnLoop.addEventListener('click', () => {
                isLooping = !isLooping;
                updateUI();
            });

            speedSelect.addEventListener('change', (e) => {
                timeScale = parseFloat(e.target.value);
            });

            timeline.addEventListener('input', (e) => {
                currentTime = parseFloat(e.target.value);
                updateUI();
            });

            canvas.addEventListener('click', () => {
                if (currentTime >= T_END) currentTime = 0.0;
                isPlaying = !isPlaying;
                updateUI();
            });

            // Keyboard Controls
            window.addEventListener('keydown', (e) => {
                if (e.code === 'Space') {
                    e.preventDefault();
                    if (currentTime >= T_END) currentTime = 0.0;
                    isPlaying = !isPlaying;
                    updateUI();
                } else if (e.code === 'KeyR') {
                    currentTime = 0.0;
                    isPlaying = true;
                    updateUI();
                }
            });

            // Start animation loop
            updateUI();
            requestAnimationFrame((timestamp) => {
                lastTimestamp = timestamp;
                animate(timestamp);
            });
        };
    </script>
</body>
</html>
