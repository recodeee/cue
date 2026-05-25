import asyncio
import concurrent.futures

import pytest

from hydra.budget import Budget, BudgetExceeded, TokenUsage


def test_charge_below_cap_succeeds() -> None:
    b = Budget(hard_cap_usd=2.00, soft_cap_usd=1.10)
    b.charge(TokenUsage(input=1000, output=500), price_in=3e-6, price_out=15e-6)
    assert b.spent_usd == pytest.approx(1000 * 3e-6 + 500 * 15e-6)


def test_charge_exceeds_hard_cap_raises() -> None:
    b = Budget(hard_cap_usd=0.01, soft_cap_usd=0.005)
    with pytest.raises(BudgetExceeded) as exc:
        b.charge(TokenUsage(input=100_000, output=1_000), price_in=3e-6, price_out=15e-6)
    assert exc.value.spent > 0.01


def test_soft_cap_warning_emitted() -> None:
    b = Budget(hard_cap_usd=2.00, soft_cap_usd=0.01)
    b.charge(TokenUsage(input=10_000, output=0), price_in=3e-6, price_out=15e-6)
    assert b.soft_cap_hit is True
    assert b.spent_usd < 2.00  # didn't trip hard cap


@pytest.mark.asyncio
async def test_concurrent_charges_respect_lock() -> None:
    b = Budget(hard_cap_usd=0.10, soft_cap_usd=0.05)

    async def charge_small() -> None:
        b.charge(TokenUsage(input=1000, output=100), price_in=3e-6, price_out=15e-6)

    await asyncio.gather(*[charge_small() for _ in range(5)])
    # Each call: 1000*3e-6 + 100*15e-6 = 0.0045; 5 calls = 0.0225
    assert 0.022 < b.spent_usd < 0.023


def test_budget_exceeded_carries_context() -> None:
    b = Budget(hard_cap_usd=0.001, soft_cap_usd=0.0005)
    try:
        b.charge(TokenUsage(input=1_000_000, output=0), price_in=3e-6, price_out=15e-6)
    except BudgetExceeded as exc:
        assert exc.max == 0.001
        assert exc.spent > 0.001


def test_concurrent_charges_respect_lock_threads() -> None:
    b = Budget(hard_cap_usd=1.00, soft_cap_usd=0.50)

    def charge_once() -> None:
        b.charge(TokenUsage(input=1000, output=100), price_in=3e-6, price_out=15e-6)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(charge_once) for _ in range(50)]
        concurrent.futures.wait(futures)
    # 50 × 0.0045 = 0.225 exactly — any race-induced double-count would miss
    assert abs(b.spent_usd - 0.225) < 1e-9


def test_cache_tokens_without_price_raises() -> None:
    b = Budget(hard_cap_usd=1.00, soft_cap_usd=0.50)
    usage = TokenUsage(input=100, output=10, cache_read=50_000)
    with pytest.raises(ValueError, match="cache_read"):
        b.charge(usage, price_in=3e-6, price_out=15e-6)


def test_cache_tokens_with_price_are_charged() -> None:
    b = Budget(hard_cap_usd=1.00, soft_cap_usd=0.50)
    usage = TokenUsage(input=100, output=10, cache_read=50_000)
    b.charge(
        usage,
        price_in=3e-6,
        price_out=15e-6,
        price_cache_read=0.3e-6,
    )
    expected = 100 * 3e-6 + 10 * 15e-6 + 50_000 * 0.3e-6
    assert b.spent_usd == pytest.approx(expected)


def test_simultaneous_soft_and_hard_cap_sets_flag_before_raise() -> None:
    b = Budget(hard_cap_usd=0.010, soft_cap_usd=0.005)
    # Single charge crosses both caps.
    with pytest.raises(BudgetExceeded):
        b.charge(
            TokenUsage(input=10_000, output=0),
            price_in=3e-6,  # 0.03 projected — crosses both
            price_out=15e-6,
        )
    # Soft-cap flag must be set even though hard-cap raised.
    assert b.soft_cap_hit is True
    # spent_usd still rolled back (raise before assignment).
    assert b.spent_usd == 0.0
