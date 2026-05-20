from backend.app.generation.prompt_variants import get_prompt_variant, get_prompt_variants


def test_prompt_variants_include_expected_ids() -> None:
    variant_ids = {variant.variant_id for variant in get_prompt_variants()}

    assert "editorial_empty_hand_v1" in variant_ids
    assert "natural_side_carry_space_v1" in variant_ids
    assert "minimal_accessory_free_v1" in variant_ids


def test_prompt_variant_metadata_targets_empty_product_space() -> None:
    variant = get_prompt_variant("editorial_empty_hand_v1")

    assert variant is not None
    assert any("empty" in addition for addition in variant.positive_additions)
    assert "bag" in variant.negative_additions
    assert "purse" in variant.negative_additions
