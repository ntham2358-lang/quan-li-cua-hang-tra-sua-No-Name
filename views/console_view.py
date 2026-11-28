class ConsoleView:
    def show(self, ok: bool, payload):
        tag = "[THÀNH CÔNG]" if ok else "[LỖI]"
        print(f"{tag} {payload}")