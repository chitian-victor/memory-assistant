all:
	# 生成的 dist/app.app 就是你的软件了
	pyinstaller -D --noconsole --name memory-assistant -y --clean  --paths . v2/app.py