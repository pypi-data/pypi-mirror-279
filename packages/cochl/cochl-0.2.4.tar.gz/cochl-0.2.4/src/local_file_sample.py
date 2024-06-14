import cochl.sense as sense


def main():
    api_config = sense.APIConfig(
        host="http://127.0.0.1:8000",
    )
    client = sense.FileClient(
        "xl8",
        api_config=api_config,
    )

    # results = client.predict("../samples/sample_gunshot.wav", timeout=0.1)
    # results = client.predict("../samples/872.mp3", timeout=1.0)
    results = client.predict("../samples/577.mp3", timeout=2.0)
    print(results.to_dict())
    print(results.to_summarized_result())


if __name__ == "__main__":
    main()
