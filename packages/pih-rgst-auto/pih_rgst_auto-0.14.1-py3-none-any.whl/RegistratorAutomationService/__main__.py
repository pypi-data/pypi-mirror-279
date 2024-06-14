import ipih

def start() -> None:
    from RegistratorAutomationService.service import start
    start(True)

if __name__ == "__main__":
    start()