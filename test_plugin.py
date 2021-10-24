import pytest

from flake8_escaping_style import (
    EscapeStyle,
    PluginError,
    StringLiteral,
)



@pytest.mark.parametrize("expected_errors,literal", [
    (PluginError.ESC101, StringLiteral.make_str(r'm\351moire')),
    (PluginError.ESC102, StringLiteral.make_str(r'm\xe9moire')),
    (PluginError.ESC103, StringLiteral.make_str(r'm\u00e9moire')),
    (PluginError.ESC104, StringLiteral.make_str(r'm\U000000e9moire')),
    (PluginError.ESC105, StringLiteral.make_str(r'm\N{latin small letter e with acute}moire')),

    ([PluginError.ESC102] * 2, StringLiteral(body=r'm\xe9moire m\xe9moire')),
    ([PluginError.ESC102] * 2, StringLiteral.make_str('m\\xe9moire\nm\\xe9moire')),

    ([], StringLiteral.make_str(r'm\xe9moire', raw=True)),
    ([], StringLiteral.make_str(r'm\\xe9moire')),

    (PluginError.ESC201, StringLiteral.make_bytes(r'm\351moire')),
    (PluginError.ESC202, StringLiteral.make_bytes(r'm\xe9moire')),

    ([], StringLiteral.make_bytes(r'm\351moire', raw=True)),
    ([], StringLiteral.make_bytes(r'm\xe9moire', raw=True)),
])
def test_escape_styles(expected_errors, literal):
    if isinstance(expected_errors, PluginError):
        expected_errors = [expected_errors]
    assert [err for err, _ in literal.escapes] == expected_errors
