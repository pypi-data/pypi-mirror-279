from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
AioHttpClientInstrumentor().instrument()

if __name__ == "__main__":
    from .app import main

    main()
