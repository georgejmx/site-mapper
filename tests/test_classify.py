from server.classify import site_to_matrix, find_site_similarity


def test_site_to_matrix():
    """Checks that Bert-Emo functions correctly"""
    result = site_to_matrix("this is a test. " * 20)
    assert isinstance(result, list)


def test_find_site_similarity():
    """Checks the logic for comparing two sites"""
    test_site_1 = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]]
    test_site_2 = [[0.11, 0.21, 0.31], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]]
    score = find_site_similarity(test_site_1, test_site_2)
    assert score > 0.5 and score < 1
