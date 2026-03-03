const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Eingaben werden in einem Status-Objekt gespeichert.
const keys = {
  left: false,
  right: false,
  thrust: false,
  fire: false,
};

// Globale Spielparameter für ein leicht verständliches Feintuning.
const SETTINGS = {
  rotationSpeed: 0.085,
  thrustPower: 0.13,
  friction: 0.992,
  laserSpeed: 8,
  laserCooldown: 180,
  spawnInterval: 1600,
  invulnerabilityMs: 1800,
  maxLives: 3,
};

let stars = [];
let asteroids = [];
let lasers = [];

let score = 0;
let lives = SETTINGS.maxLives;
let gameOver = false;
let lastShotAt = 0;
let lastSpawnAt = 0;
let lastFrameTime = 0;
let currentSpawnInterval = SETTINGS.spawnInterval;

const ship = {
  x: 0,
  y: 0,
  vx: 0,
  vy: 0,
  angle: -Math.PI / 2,
  radius: 15,
  invulnerableUntil: 0,
};

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  createStarfield();

  // Schiff bei Resize in die Mitte setzen, damit es nie außerhalb landet.
  ship.x = canvas.width / 2;
  ship.y = canvas.height / 2;
}

function createStarfield() {
  const starCount = Math.max(120, Math.floor((canvas.width * canvas.height) / 9000));
  stars = Array.from({ length: starCount }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    size: Math.random() * 2 + 0.3,
    alpha: Math.random() * 0.7 + 0.2,
  }));
}

function drawStars() {
  ctx.save();
  for (const star of stars) {
    ctx.globalAlpha = star.alpha;
    ctx.fillStyle = "#d8e3ff";
    ctx.beginPath();
    ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();
}

function wrap(obj) {
  if (obj.x < -obj.radius) obj.x = canvas.width + obj.radius;
  if (obj.x > canvas.width + obj.radius) obj.x = -obj.radius;
  if (obj.y < -obj.radius) obj.y = canvas.height + obj.radius;
  if (obj.y > canvas.height + obj.radius) obj.y = -obj.radius;
}

function randomEdgePosition() {
  const edge = Math.floor(Math.random() * 4);
  if (edge === 0) return { x: Math.random() * canvas.width, y: -20 }; // oben
  if (edge === 1) return { x: canvas.width + 20, y: Math.random() * canvas.height }; // rechts
  if (edge === 2) return { x: Math.random() * canvas.width, y: canvas.height + 20 }; // unten
  return { x: -20, y: Math.random() * canvas.height }; // links
}

function createAsteroid(stage, x, y) {
  const radiusByStage = [18, 32, 52];
  const speedByStage = [2.4, 1.7, 1.2];
  const angle = Math.random() * Math.PI * 2;
  const wobble = (Math.random() - 0.5) * 0.5;

  return {
    x,
    y,
    vx: Math.cos(angle) * speedByStage[stage] + wobble,
    vy: Math.sin(angle) * speedByStage[stage] + wobble,
    radius: radiusByStage[stage],
    stage,
    // Raue Kontur für klassischen Asteroiden-Look.
    shape: Array.from({ length: 10 }, (_, i) => ({
      angle: (Math.PI * 2 * i) / 10,
      offset: 0.75 + Math.random() * 0.45,
    })),
  };
}

function spawnAsteroid() {
  if (gameOver) return;
  const pos = randomEdgePosition();
  asteroids.push(createAsteroid(2, pos.x, pos.y));
}

function splitAsteroid(index) {
  const asteroid = asteroids[index];

  if (asteroid.stage > 0) {
    for (let i = 0; i < 2; i++) {
      asteroids.push(createAsteroid(asteroid.stage - 1, asteroid.x, asteroid.y));
    }
  }

  score += (3 - asteroid.stage) * 100;
  asteroids.splice(index, 1);
}

function drawShip(now) {
  const isInvulnerable = now < ship.invulnerableUntil;
  if (isInvulnerable && Math.floor(now / 80) % 2 === 0) return;

  ctx.save();
  ctx.translate(ship.x, ship.y);
  ctx.rotate(ship.angle + Math.PI / 2);

  ctx.strokeStyle = "#f5f7ff";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, -ship.radius);
  ctx.lineTo(ship.radius * 0.75, ship.radius);
  ctx.lineTo(0, ship.radius * 0.45);
  ctx.lineTo(-ship.radius * 0.75, ship.radius);
  ctx.closePath();
  ctx.stroke();

  // Flamme wird nur beim Schub gezeigt.
  if (keys.thrust && !gameOver) {
    ctx.strokeStyle = "#ffb347";
    ctx.beginPath();
    ctx.moveTo(-5, ship.radius - 1);
    ctx.lineTo(0, ship.radius + 10 + Math.random() * 6);
    ctx.lineTo(5, ship.radius - 1);
    ctx.stroke();
  }

  ctx.restore();
}

function drawAsteroids() {
  ctx.strokeStyle = "#9db0d8";
  ctx.lineWidth = 2;

  for (const asteroid of asteroids) {
    ctx.save();
    ctx.translate(asteroid.x, asteroid.y);
    ctx.beginPath();

    asteroid.shape.forEach((point, idx) => {
      const px = Math.cos(point.angle) * asteroid.radius * point.offset;
      const py = Math.sin(point.angle) * asteroid.radius * point.offset;
      if (idx === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    });

    ctx.closePath();
    ctx.stroke();
    ctx.restore();
  }
}

function drawLasers() {
  ctx.fillStyle = "#ff5f5f";
  for (const laser of lasers) {
    ctx.beginPath();
    ctx.arc(laser.x, laser.y, 2.3, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawHUD() {
  ctx.fillStyle = "#dfe7ff";
  ctx.font = "bold 22px Trebuchet MS, sans-serif";
  ctx.textAlign = "left";
  ctx.fillText(`Score: ${score}`, 18, 34);

  ctx.textAlign = "right";
  ctx.fillText(`Lives: ${lives}`, canvas.width - 18, 34);

  if (gameOver) {
    ctx.textAlign = "center";
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 54px Trebuchet MS, sans-serif";
    ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 8);
    ctx.font = "24px Trebuchet MS, sans-serif";
    ctx.fillStyle = "#bccbff";
    ctx.fillText("Drücke R für Neustart", canvas.width / 2, canvas.height / 2 + 34);
  }
}

function updateShip(now) {
  if (gameOver) return;

  if (keys.left) ship.angle -= SETTINGS.rotationSpeed;
  if (keys.right) ship.angle += SETTINGS.rotationSpeed;

  if (keys.thrust) {
    ship.vx += Math.cos(ship.angle) * SETTINGS.thrustPower;
    ship.vy += Math.sin(ship.angle) * SETTINGS.thrustPower;
  }

  ship.vx *= SETTINGS.friction;
  ship.vy *= SETTINGS.friction;

  ship.x += ship.vx;
  ship.y += ship.vy;

  wrap(ship);

  if (keys.fire && now - lastShotAt > SETTINGS.laserCooldown) {
    lasers.push({
      x: ship.x + Math.cos(ship.angle) * ship.radius,
      y: ship.y + Math.sin(ship.angle) * ship.radius,
      vx: Math.cos(ship.angle) * SETTINGS.laserSpeed + ship.vx * 0.2,
      vy: Math.sin(ship.angle) * SETTINGS.laserSpeed + ship.vy * 0.2,
      radius: 2,
      life: 70,
    });
    lastShotAt = now;
  }
}

function updateAsteroids() {
  for (const asteroid of asteroids) {
    asteroid.x += asteroid.vx;
    asteroid.y += asteroid.vy;
    wrap(asteroid);
  }
}

function updateLasers() {
  for (let i = lasers.length - 1; i >= 0; i--) {
    const laser = lasers[i];
    laser.x += laser.vx;
    laser.y += laser.vy;
    laser.life -= 1;
    wrap(laser);

    if (laser.life <= 0) {
      lasers.splice(i, 1);
      continue;
    }

    for (let j = asteroids.length - 1; j >= 0; j--) {
      const asteroid = asteroids[j];
      const dx = laser.x - asteroid.x;
      const dy = laser.y - asteroid.y;
      const dist = Math.hypot(dx, dy);

      if (dist < asteroid.radius + laser.radius) {
        lasers.splice(i, 1);
        splitAsteroid(j);
        break;
      }
    }
  }
}

function checkShipCollision(now) {
  if (gameOver || now < ship.invulnerableUntil) return;

  for (const asteroid of asteroids) {
    const dx = ship.x - asteroid.x;
    const dy = ship.y - asteroid.y;
    const dist = Math.hypot(dx, dy);

    if (dist < ship.radius + asteroid.radius * 0.78) {
      lives -= 1;
      ship.invulnerableUntil = now + SETTINGS.invulnerabilityMs;

      // Nach Treffer wird das Schiff neu positioniert und etwas abgebremst.
      ship.x = canvas.width / 2;
      ship.y = canvas.height / 2;
      ship.vx *= 0.25;
      ship.vy *= 0.25;

      if (lives <= 0) {
        lives = 0;
        gameOver = true;
      }
      break;
    }
  }
}

function maybeSpawnAsteroids(now) {
  if (gameOver) return;

  const dynamicLimit = 4 + Math.floor(score / 1200);
  if (asteroids.length < dynamicLimit && now - lastSpawnAt > currentSpawnInterval) {
    spawnAsteroid();
    lastSpawnAt = now;

    // Mit höherem Score spawnen Asteroiden etwas schneller.
    currentSpawnInterval = Math.max(550, SETTINGS.spawnInterval - Math.floor(score / 8));
  }
}

function resetGame() {
  score = 0;
  lives = SETTINGS.maxLives;
  gameOver = false;
  asteroids = [];
  lasers = [];
  lastSpawnAt = 0;
  lastShotAt = 0;
  currentSpawnInterval = SETTINGS.spawnInterval;

  ship.x = canvas.width / 2;
  ship.y = canvas.height / 2;
  ship.vx = 0;
  ship.vy = 0;
  ship.angle = -Math.PI / 2;
  ship.invulnerableUntil = performance.now() + SETTINGS.invulnerabilityMs;

  for (let i = 0; i < 3; i++) {
    spawnAsteroid();
  }
}

function gameLoop(timestamp) {
  const now = timestamp || performance.now();
  const delta = now - lastFrameTime;
  lastFrameTime = now;

  // Delta wird aktuell nur zur Stabilisierung bei erstem Frame berücksichtigt.
  if (!Number.isFinite(delta)) {
    requestAnimationFrame(gameLoop);
    return;
  }

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawStars();

  updateShip(now);
  updateAsteroids();
  updateLasers();
  checkShipCollision(now);
  maybeSpawnAsteroids(now);

  drawAsteroids();
  drawLasers();
  drawShip(now);
  drawHUD();

  requestAnimationFrame(gameLoop);
}

window.addEventListener("keydown", (event) => {
  const key = event.key.toLowerCase();

  if (["arrowleft", "arrowright", "arrowup", " ", "spacebar", "r"].includes(key)) {
    event.preventDefault();
  }

  if (key === "arrowleft") keys.left = true;
  if (key === "arrowright") keys.right = true;
  if (key === "arrowup") keys.thrust = true;
  if (key === " " || key === "spacebar") keys.fire = true;

  if (key === "r") {
    resetGame();
  }
});

window.addEventListener("keyup", (event) => {
  const key = event.key.toLowerCase();
  if (key === "arrowleft") keys.left = false;
  if (key === "arrowright") keys.right = false;
  if (key === "arrowup") keys.thrust = false;
  if (key === " " || key === "spacebar") keys.fire = false;
});

window.addEventListener("resize", resizeCanvas);

resizeCanvas();
resetGame();
requestAnimationFrame(gameLoop);
