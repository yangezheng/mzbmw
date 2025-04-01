#!/usr/bin/env bash
# Install poetry
pip install poetry
poetry config virtualenvs.create false
poetry install --no-root

# Install Playwright dependencies
apt-get update
apt-get install -y --no-install-recommends \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libcups2 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgdk-pixbuf-2.0-0 \
    libgbm1 \
    libxshmfence1 \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libnspr4 \
    libnss3 \
    xdg-utils \
    wget

# Install Playwright and browsers explicitly with system dependencies
pip install playwright
python -m playwright install --with-deps chromium
python -m playwright install-deps
python -m playwright install chromium

# Create needed directories for Playwright browser
mkdir -p /tmp/playwright-browsers
chmod -R 777 /tmp/playwright-browsers
