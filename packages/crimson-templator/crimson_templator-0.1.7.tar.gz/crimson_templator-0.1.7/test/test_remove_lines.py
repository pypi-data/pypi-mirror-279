from crimson.templator import remove_lines

template = r'''
must start with 6 after remove
\(remove_below: 5\)
1
2
3
4
5
6
7
8

6
5
4
3
2
1
\(remove_above:2\)
must start with 3 after remove

'''

# The last one line is missing.
# Should I debug it?
expected = r'''
must start with 6 after remove
6
7
8

6
5
4
3
must start with 3 after remove

'''


def test_remove_lines():
    after_remove = remove_lines(
        template=template,
        open=r"\(",
        close=r"\)"
    )

    assert after_remove == expected