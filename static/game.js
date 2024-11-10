class HexGrid {
    constructor(size = 30) {
        this.size = size;
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.setupCanvas();
        this.setupEventListeners();
    }

    setupCanvas() {
        this.canvas.width = 800;
        this.canvas.height = 600;
        this.centerX = this.canvas.width / 2;
        this.centerY = this.canvas.height / 2;
    }

    setupEventListeners() {
        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const hex = this.pixelToHex(x - this.centerX, y - this.centerY);
            this.handleHexClick(hex);
        });
    }

    pixelToHex(x, y) {
        const q = (2/3 * x) / this.size;
        const r = (-1/3 * x + Math.sqrt(3)/3 * y) / this.size;
        return this.roundHex(q, r);
    }

    roundHex(q, r) {
        let s = -q - r;
        let rq = Math.round(q);
        let rr = Math.round(r);
        let rs = Math.round(s);

        const qDiff = Math.abs(rq - q);
        const rDiff = Math.abs(rr - r);
        const sDiff = Math.abs(rs - s);

        if (qDiff > rDiff && qDiff > sDiff) {
            rq = -rr - rs;
        } else if (rDiff > sDiff) {
            rr = -rq - rs;
        }

        return { q: rq, r: rr };
    }

    hexToPixel(q, r) {
        const x = this.size * (3/2 * q);
        const y = this.size * (Math.sqrt(3)/2 * q + Math.sqrt(3) * r);
        return { x: x + this.centerX, y: y + this.centerY };
    }

    drawHex(x, y, color = '#333333') {
        this.ctx.beginPath();
        for (let i = 0; i < 6; i++) {
            const angle = 2 * Math.PI / 6 * i;
            const xPos = x + this.size * Math.cos(angle);
            const yPos = y + this.size * Math.sin(angle);
            if (i === 0) {
                this.ctx.moveTo(xPos, yPos);
            } else {
                this.ctx.lineTo(xPos, yPos);
            }
        }
        this.ctx.closePath();
        this.ctx.fillStyle = color;
        this.ctx.fill();
        this.ctx.strokeStyle = '#666666';
        this.ctx.stroke();
    }

    async handleHexClick(hex) {
        try {
            const response = await fetch('/api/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(hex)
            });
            const data = await response.json();
            if (data.success) {
                this.redraw();
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    redraw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        // Draw grid
        for (let q = -5; q <= 5; q++) {
            for (let r = -5; r <= 5; r++) {
                const { x, y } = this.hexToPixel(q, r);
                this.drawHex(x, y);
            }
        }
        // Draw player
        const playerPos = this.hexToPixel(0, 0);
        this.ctx.beginPath();
        this.ctx.arc(playerPos.x, playerPos.y, 10, 0, 2 * Math.PI);
        this.ctx.fillStyle = '#ff0000';
        this.ctx.fill();
    }
}

const game = new HexGrid();
game.redraw();