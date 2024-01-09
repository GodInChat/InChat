#!/bin/sh

export HOST=0.0.0.0
export PORT=8001
export OLLAMA_URL=http://172.27.72.6:11434

uvicorn main:app --host=$HOST --port=$PORT --reload
