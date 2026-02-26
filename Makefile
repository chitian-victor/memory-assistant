all:
	# 生成的 dist/app.app 就是你的软件了
	pyinstaller -D --noconsole --paths . v2/app.py