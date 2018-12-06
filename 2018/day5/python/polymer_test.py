import polymer


def test_reduce_polymer():
    assert polymer.reduce_polymer('dabAcCaCBAcCcaDA') == 'dabCBAcaDA'
    assert polymer.reduce_polymer('abACcBadDACae') == 'abABCae'
    assert polymer.reduce_polymer('abBA') == ''
    assert polymer.reduce_polymer('aA') == ''
    assert polymer.reduce_polymer('') == ''


def test_test_for_annihilation():
    assert polymer.test_for_annihilation('a', 'A')
    assert polymer.test_for_annihilation('A', 'a')
    assert polymer.test_for_annihilation('Z', 'z')

    assert not polymer.test_for_annihilation('Z', 'A')
    assert not polymer.test_for_annihilation('a', 'Z')
    assert not polymer.test_for_annihilation('a', 'z')
    assert not polymer.test_for_annihilation('Z', 'Z')
