.PHONY: install-rye-zsh install-rye-bash launch

install-rye-zsh:
	curl -sSf https://rye-up.com/get | bash \
	&& echo 'source "$$HOME/.rye/env"' >> ~/.zshrc

install-rye-bash:
	curl -sSf https://rye-up.com/get | bash \
	&& echo 'source "$$HOME/.rye/env"' >> ~/.bashrc


launch:
	rye run python main.py
