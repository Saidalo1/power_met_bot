compile:
	@echo "Compiling translations..."
	@pybabel compile -d locales
	@echo "Translations compiled successfully"

compile_mo:
	@echo "Compiling messages.mo from messages.po"
	@msgfmt -o locales/en/LC_MESSAGES/messages.mo locales/en/LC_MESSAGES/messages.po
	@echo "messages.po compiled successfully"
