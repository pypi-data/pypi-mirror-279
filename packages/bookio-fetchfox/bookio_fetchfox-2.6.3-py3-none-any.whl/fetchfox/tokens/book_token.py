from fetchfox.constants.book import (
    BOOK_TOKEN_ASSET_ID,
    BOOK_TOKEN_ASSET_NAME,
    BOOK_TOKEN_COINGECKO_ID,
    BOOK_TOKEN_POLICY_ID,
    BOOK_TOKEN_FINGERPRINT,
)
from fetchfox.constants.currencies import BOOK

from .base import CardanoToken


class BookToken(CardanoToken):
    def __init__(self, dexhunterio_partner_code: str):
        super().__init__(
            asset_id=BOOK_TOKEN_ASSET_ID,
            asset_name=BOOK_TOKEN_ASSET_NAME,
            fingerprint=BOOK_TOKEN_FINGERPRINT,
            policy_id=BOOK_TOKEN_POLICY_ID,
            symbol=BOOK,
            decimals=6,
            coingecko_id=BOOK_TOKEN_COINGECKO_ID,
            taptools_pair_id="2ed309a7ecb6d0d5e00dca0bcc3924fdc0627a5fb631f1acc4deb898b14ee8bd",
            dexhunterio_partner_code=dexhunterio_partner_code,
        )
