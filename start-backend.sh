#!/bin/bash
cd /home/jdvalmart/proyectos/PequeLectores_inteligente_por_IA/backend
source .venv/bin/activate
exec uvicorn app.main:app --host 0.0.0.0 --port 8000