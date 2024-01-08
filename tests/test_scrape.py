from server.scrape import scrape_site

TARGET_URL = "https://georgejmx.dev"


def test_scrape_site():
    """Checks that sites are correctly scraped"""
    expected_content = "DIY developer with a passion for technology and creativity."
    result = scrape_site(TARGET_URL)
    assert result[0].startswith(expected_content)

    flat_result = scrape_site(TARGET_URL, False)
    assert flat_result[0].startswith(expected_content)
