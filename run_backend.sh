#!/bin/bash
# run_backend.sh
# AI-Powered Wheat Farming Assistant
# Amina Habiba — 2022-ag-7802 — UAF Faisalabad — 2026
#
# This file is for Linux/Mac users only.
# Windows users: use start_app.bat instead.
#
# Usage on Linux/Mac:
#   bash run_backend.sh

echo "Starting Ollama..."
ollama serve &
sleep 5

echo "Starting Flask Backend..."
python backend/app.py