import requests
from sources.base_source import MarketSource


class SECSource(MarketSource):
    name = "SEC EDGAR"
    source_type = "SEC Filing"

    TICKER_LOOKUP_URL = "https://www.sec.gov/files/company_tickers.json"
    SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"

    IMPORTANT_FORMS = {
        "8-K": {
            "description": "Current report / material event",
            "importance": "High",
            "event_type": "Material Event",
        },
        "10-Q": {
            "description": "Quarterly report",
            "importance": "High",
            "event_type": "Earnings / Financial Report",
        },
        "10-K": {
            "description": "Annual report",
            "importance": "High",
            "event_type": "Annual Financial Report",
        },
        "4": {
            "description": "Insider transaction",
            "importance": "Medium",
            "event_type": "Insider Activity",
        },
        "S-1": {
            "description": "Registration statement",
            "importance": "High",
            "event_type": "Share Offering / Registration",
        },
        "DEF 14A": {
            "description": "Proxy statement",
            "importance": "Medium",
            "event_type": "Governance / Shareholder Vote",
        },
    }

    def __init__(self):
        self.headers = {
            "User-Agent": "insider-app-prototype contact@example.com"
        }
        self.ticker_cache = None

    def fetch(self, ticker: str, limit: int = 10):
        ticker = ticker.upper()
        cik = self.get_cik_for_ticker(ticker)

        if not cik:
            print(f"No SEC CIK found for {ticker}")
            return []

        return self.get_recent_filings(cik, ticker, limit)

    def get_cik_for_ticker(self, ticker: str):
        try:
            if self.ticker_cache is None:
                response = requests.get(
                    self.TICKER_LOOKUP_URL,
                    headers=self.headers,
                    timeout=10,
                )
                response.raise_for_status()
                self.ticker_cache = response.json()

            for _, company in self.ticker_cache.items():
                if company.get("ticker", "").upper() == ticker:
                    return str(company.get("cik_str", "")).zfill(10)

        except Exception as e:
            print(f"SEC ticker lookup error: {e}")

        return None

    def get_recent_filings(self, cik: str, ticker: str, limit: int):
        items = []

        try:
            url = self.SUBMISSIONS_URL.format(cik=cik)

            response = requests.get(
                url,
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()

            data = response.json()
            company_name = data.get("name", ticker)

            recent = data.get("filings", {}).get("recent", {})

            forms = recent.get("form", [])
            filing_dates = recent.get("filingDate", [])
            accession_numbers = recent.get("accessionNumber", [])
            primary_documents = recent.get("primaryDocument", [])

            for form, filing_date, accession, primary_doc in zip(
                forms,
                filing_dates,
                accession_numbers,
                primary_documents,
            ):
                if form not in self.IMPORTANT_FORMS:
                    continue

                form_info = self.IMPORTANT_FORMS[form]

                clean_accession = accession.replace("-", "")

                filing_url = (
                    f"https://www.sec.gov/Archives/edgar/data/"
                    f"{int(cik)}/{clean_accession}/{primary_doc}"
                )

                title = (
                    f"{ticker} filed {form} on {filing_date}: "
                    f"{form_info['description']}"
                )

                items.append({
                    "title": title,
                    "publisher": "SEC EDGAR",
                    "link": filing_url,
                    "source_type": self.source_type,
                    "text": (
                        f"{company_name} filed SEC form {form}. "
                        f"Event type: {form_info['event_type']}. "
                        f"Importance: {form_info['importance']}."
                    ),
                    "filing_type": form,
                    "filing_date": filing_date,
                    "event_type": form_info["event_type"],
                    "importance": form_info["importance"],
                })

                if len(items) >= limit:
                    break

        except Exception as e:
            print(f"SEC filings source error: {e}")

        return items