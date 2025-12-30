from __future__ import annotations

import supriya


def test_gatogen_anthem_build_score_uses_render(tmp_path, monkeypatch) -> None:
    import scripts.gatogen_anthem_01 as gatogen

    called = {}

    def fake_render(score, output_file_path, header_format):
        called["score"] = score
        called["output_file_path"] = output_file_path
        called["header_format"] = header_format
        return output_file_path, 0

    monkeypatch.setattr(supriya, "render", fake_render)

    output_path = tmp_path / "gatogen.wav"
    rendered_path, exit_code = gatogen.build_score(output_path)

    assert exit_code == 0
    assert rendered_path == output_path
    assert output_path.parent.exists()
    assert called["output_file_path"] == output_path
    assert called["header_format"] == "wav"
