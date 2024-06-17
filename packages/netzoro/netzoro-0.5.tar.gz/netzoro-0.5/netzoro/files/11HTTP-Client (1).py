from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.client import readBody


def download_web_page(url):
    agent = Agent(reactor)

    def handle_response(response):
        d = readBody(response)
        d.addCallback(lambda body: print(body.decode()))
        d.addBoth(lambda _: reactor.stop())

    def handle_error(error):
        print(f"An error occurred: {error}")
        reactor.stop()

    d = agent.request(b"GET", url.encode())
    d.addCallbacks(handle_response, handle_error)

    reactor.run()


if __name__ == "__main__":
    download_web_page("http://www.google.com/")

