#!/bin/sh

python3 dbtest-sql.py
RC=$?
if [ "$RC" -ne 0 ]; then
    if [ "$RC" -eq 100 ]; then
	echo "# alembic upgrade head"
	! alembic upgrade head && exit 1
    else
	exit 1
    fi
fi

python3 dbtest-vec.py
RC=$?
[ "$RC" -ne 0 -a "$RC" -ne 100 ] && exit 1

[ -z "$HOST" ] && HOST=0.0.0.0
[ -z "$PORT" ] && PORT=8000

uvicorn main:app --host=$HOST --port=$PORT --reload
